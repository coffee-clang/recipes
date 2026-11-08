#!/usr/bin/env python3
"""Lint the shell scripts that ship with each recipe.

Catches the defects that make a recipe fail at install time rather than at
review time: syntax errors, unquoted expansions, undeclared build tools,
rolling-branch versions, and shared libraries that were never enabled.
"""

import re
import shlex
import shutil
import string
import subprocess
import tempfile
import unittest
from pathlib import Path

from check_dependencies import HOST_TOOLS
from recipe_metadata import RECIPES_DIR, load_recipe, recipe_files
import recipe_script
from recipe_script import header_assignments

# Branch and channel names that are not versions. A recipe pinned to one of
# these is not reproducible and must name a tag, release, or commit.
BRANCH_NAMES = frozenset({
    "stable", "main", "master", "head", "latest", "trunk", "dev", "nightly",
})

# Commands an install.sh may invoke that are not part of the recipe's own
# dependency list. These are assumed present on any POSIX host.
BASE_TOOLS = frozenset({
    "bash", "sh", "cd", "mkdir", "rm", "cp", "mv", "ls", "cat", "echo", "test",
    "wget", "curl", "tar", "unzip", "git", "make", "install", "basename",
    "dirname", "sed", "grep", "awk", "true", "false", "chmod", "nproc",
})

# Recipes that only download sources yet still declare build tools they never
# invoke. This is metadata debt, enumerated rather than skipped: a recipe
# leaving the set (because it was fixed) or joining it (because a new one was
# copied from an old recipe) fails EXPECTED_FETCH_ONLY_WITH_BUILD_DEPS below, so
# the debt can neither grow nor shrink unnoticed.
EXPECTED_FETCH_ONLY_WITH_BUILD_DEPS = frozenset({
    "attr", "blas", "brotli", "c-ares", "fribidi", "jansson", "json-c",
    "libjpeg-turbo", "libuv", "lz4", "opus", "pcre2", "wavpack", "yajl",
    "zeromq", "zstd",
})

# Recipes whose build system defaults to a static-only build, so they must opt
# in to shared libraries explicitly. Pinned exactly: a second such recipe has
# to be handled here rather than silently skipped by the shared-library guard.
EXPECTED_STATIC_BY_DEFAULT = frozenset({"x264"})

# A glob in cd is only safe when it is confined to a directory we created and
# restricted to directories with a trailing slash.
SAFE_CD_GLOB = re.compile(r'^cd "\$PREFIX"/src/\*/$')

# A bare $VAR expansion. Deliberately does not match $(...): that is a
# substitution, not a word-splitting hazard. ${...} is matched: unquoted it
# word-splits exactly like $VAR.
EXPANSION = re.compile(r'(?<![\w$\\{`])\$\{?[A-Za-z_][A-Za-z0-9_]*\}?')

# Command substitutions and quoted spans, innermost first. Removing them
# before scanning for bare expansions is what keeps an expansion that sits
# mid-string inside quotes (cd "$PREFIX/lib-${VERSION}") from being mistaken
# for an unquoted one. ${...} is deliberately not stripped: it is a parameter
# expansion, and unquoted it word-splits exactly like $VAR.
NESTED = re.compile(r"\$\([^()]*\)")
QUOTED = re.compile(r'"[^"]*"|\'[^\']*\'')

# Assignments do not word-split, so a bare expansion on the right-hand side of
# an assignment is safe. Imported rather than redefined: a second copy would
# let the rule checked here drift from the one header_assignments() applies.
ASSIGNMENT = recipe_script.ASSIGNMENT

# git clone must name an explicit destination: without one, the checkout lands
# in the upstream repo's basename, which need not match $PACKAGE. The pattern
# is anchored to a command position (start of line or after a chain operator
# like ;, &&, ||) and the destination must be the clone's own argument:
# [^&|;]* cannot cross a chain operator, so a "$PACKAGE" in a later command
# does not count. What follows the destination is not checked, only that the
# destination argument is present: a trailing comment, chained command, pipe,
# or subshell close is fine. The lookahead also accepts / so a destination
# used as a path prefix ("$PACKAGE"/sub) is not a false positive. A
# commented-out clone line is not a clone at all: the leading # cannot be
# crossed because the anchor matches only ^ or an operator. (A comment
# containing an operator before a clone, e.g. "# x; git clone ...", would
# match; that is accepted as contrived.) Known boundary: the real-tree guard
# inspects only lines containing "git clone", so a clone split by a \
# continuation is not seen; accepted, not a regression.
GIT_CLONE_WITH_DEST = re.compile(
    r'(?:^|[;&|]{1,2})\s*git clone [^&|;]*"\$PACKAGE"(?=[\s;&|)/]|$)'
)


def strip_quoted(line: str) -> str:
    """Blank out substitutions and quoted spans, leaving bare expansions.

    Applied repeatedly so nested forms collapse: in
    ARCHIVE="$(basename "$URL")" the inner "$URL" disappears with its
    substitution, leaving no residue to be misread as unquoted.
    """
    previous = None
    while previous != line:
        previous = line
        line = NESTED.sub("", line)
        line = QUOTED.sub("", line)
    return line


def unquoted_expansions(line: str) -> list[str]:
    """Return the bare $VAR expansions on a line that need quoting."""
    if line.lstrip().startswith("#") or ASSIGNMENT.match(line):
        return []
    return [m.group() for m in EXPANSION.finditer(strip_quoted(line))]


def install_scripts(base_dir=RECIPES_DIR):
    """Yield (toml_file, script_path) for every recipe that ships a script."""
    for toml_file in recipe_files(base_dir):
        script = toml_file.parent / "install.sh"
        if script.exists():
            yield toml_file, script


# The letter after `x` in an operation cluster names the decompressor, so a
# probe archive has to be built with the same one or tar rejects the archive
# rather than the flags. "" is an uncompressed tar.
TAR_SUFFIX = {"": ".tar", "z": ".tar.gz", "j": ".tar.bz2", "J": ".tar.xz"}
TAR_CREATE = {"": "cf", "z": "czf", "j": "cjf", "J": "cJf"}

# A variable reference anywhere in a tar operand, quoted or not. The -C target
# is usually a compound path ("$PREFIX/src"), not a bare "$PREFIX".
# Matches an expansion together with the quotes around it, so a substituted
# token is already clean and adjacent pairs like "$A""$B" keep their own
# quoting rather than having every quote stripped from both ends.
VAR_REF = re.compile(r'"?\$\{?([A-Za-z_]\w*)\}?"?')


def compressor_flag(cluster: str) -> str | None:
    """Return the decompressor letter in a tar operation cluster, if any."""
    for letter in ("J", "j", "z"):
        if letter in cluster:
            return letter
    return None


# Long options that themselves name the operation. These may appear anywhere in
# the argument list, so they do not open the operation boundary.
TAR_OPERATION_LONG = frozenset({
    "--extract", "--get", "--create", "--list", "--append", "--update",
    "--delete", "--compare", "--diff", "--concatenate", "--incremental",
})

# Short flags that make their cluster the operation.
TAR_OPERATION_LETTERS = frozenset("xtcTaurdfjJmvzlpkw")

# What a short-flag cluster may contain. Anything else — a path, an expansion —
# is an operand, not a cluster.
SHORT_FLAG_CHARS = frozenset(string.ascii_letters + string.digits)


def short_cluster(token: str) -> str:
    """Return the letters of a short-option token, or "" if it is not one.

    A cluster may carry its own dash or none: `xzf` and `-xzf` are both valid
    tar spellings.
    """
    if token.startswith("--"):
        return ""
    flags = token[1:] if token.startswith("-") else token
    if not flags or not set(flags) <= SHORT_FLAG_CHARS:
        return ""
    return flags


def tar_operation_index(tokens: list[str]) -> int:
    """Return the index of the token that specifies tar's operation, else -1.

    Both spellings count: a cluster (`xzf`) and a long option (`--extract`).
    Any other long option is a modifier, and a modifier ahead of the operation
    is what GNU tar rejects.

    A no-dash cluster is only a cluster while no operand has appeared: tar's
    old-style parsing reads the first non-option token as the operation, so a
    bare word after an operand ("src" after "a.tar.gz") is an operand, not a
    cluster.
    """
    for index, token in enumerate(tokens):
        if token in TAR_OPERATION_LONG:
            return index
        cluster = short_cluster(token)
        if cluster and set(cluster) & TAR_OPERATION_LETTERS:
            if token.startswith("-") or all(
                t.startswith("-") for t in tokens[:index]
            ):
                return index
    return -1


def tar_invocations():
    """Yield (script, lineno, line, cluster) for every tar command."""
    for _, script in install_scripts():
        for lineno, line in enumerate(script.read_text().splitlines(), 1):
            if line.strip().startswith("tar "):
                tokens = shlex.split(line)[1:]
                yield script, lineno, line, tokens[0] if tokens else ""


def probe_archives(root: Path) -> dict:
    """Build one real archive per compression form the recipes use.

    The decompressor has to match the operation cluster, or tar rejects the
    archive instead of the flags and the probe proves nothing. Raises
    RuntimeError when the host cannot produce one form, so a caller can skip
    rather than pass quietly.
    """
    needed = {compressor_flag(cluster) or ""
              for _, _, _, cluster in tar_invocations()}
    archives = {}
    for flag in sorted(needed):
        label = flag or "plain"
        source = root / f"src-{label}"
        source.mkdir()
        (source / "payload.txt").write_text("probe")
        archive = root / f"probe-{label}{TAR_SUFFIX[flag]}"
        result = subprocess.run(
            ["tar", TAR_CREATE[flag], str(archive),
             "-C", str(source), "payload.txt"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"cannot build a {label} probe archive on this host: "
                f"{result.stderr.strip()}"
            )
        archives[flag] = archive
    return archives


def directory_operands(argv: list[str]) -> list[str]:
    """Return the directories a tar command line extracts into.

    Handles all three spellings a recipe could use: a detached `-C dir`, the
    attached `-Cdir`, and the long `--directory=dir`.
    """
    operands = []
    for index, token in enumerate(argv):
        if token == "-C":
            if index + 1 < len(argv):
                operands.append(argv[index + 1])
        elif token.startswith("--directory="):
            operands.append(token.split("=", 1)[1])
        elif token.startswith("-C") and len(token) > 2:
            operands.append(token[2:])
    return operands


def probe_tar_line(root: Path, archives: dict, line: str, cluster: str,
                   name: str):
    """Run one recipe's tar line against a probe archive, confined to `root`.

    This executes repository-controlled text for real, so the sandbox is the
    trust boundary: tar's working directory is a fresh subdirectory of `root`,
    and a `-C` operand that does not resolve inside `root` is refused rather
    than created. Recipe variables resolve to the probe's own target, so only
    a hardcoded path can escape — and a line with no `-C` at all lands in the
    working directory instead of the repository.

    Returns (result, target): the CompletedProcess and the directory tar
    extracted into, as a Path.
    """
    flag = compressor_flag(cluster) or ""
    # A private working directory and target per line, so one subTest cannot
    # leave a file that makes the next one pass.
    workdir = root / f"cwd-{name}"
    target = root / f"out-{name}"
    workdir.mkdir()
    values = {"ARCHIVE": str(archives[flag])}

    def resolve(match, _values=values, _target=str(target)):
        # Whatever this recipe calls its extraction directory, resolved here to
        # the per-line target.
        return str(_values.setdefault(match.group(1), _target))

    argv = [VAR_REF.sub(resolve, token) for token in shlex.split(line)[1:]]

    destinations = directory_operands(argv)
    for destination in destinations:
        path = Path(destination)
        # The lexical is_relative_to check alone is bypassable: a variable
        # resolves to a path inside root, so "$PREFIX/../../escaped" passes it
        # and then resolves outside. Compare resolved paths, and refuse any
        # operand that walks up at all. The ".." refusal is deliberately
        # stricter than the resolve() check: it also rejects a ".." that
        # resolves back inside root. That is the safe direction, and no recipe
        # needs to walk up, so the strictness costs nothing.
        if ".." in path.parts or not path.resolve().is_relative_to(
            root.resolve()
        ):
            raise AssertionError(
                f"{name}: tar would extract into {destination}, which is "
                f"outside the probe directory {root}"
            )
    # -C names a directory that must already exist, and a recipe's own
    # `mkdir -p` is not part of the line under test.
    for destination in destinations:
        Path(destination).mkdir(parents=True, exist_ok=True)

    result = subprocess.run(["tar", *argv], cwd=workdir,
                            capture_output=True, text=True)
    return result, (Path(destinations[-1]) if destinations else workdir)


class TestScriptSyntax(unittest.TestCase):
    def test_every_install_script_parses(self):
        for _, script in install_scripts():
            result = subprocess.run(["bash", "-n", str(script)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0,
                             f"{script}: {result.stderr.strip()}")

    def test_every_script_is_executable_aware(self):
        for _, script in install_scripts():
            with self.subTest(script=script.name):
                self.assertTrue(script.read_text().startswith("#!"), script)

    def test_every_script_sets_errexit(self):
        for _, script in install_scripts():
            text = script.read_text()
            self.assertIn("set -e", text, f"{script} lacks 'set -e'")

    def test_every_script_sets_pipefail(self):
        # Without pipefail, a future `wget | tar` refactor would extract an
        # empty or truncated stream and still exit 0.
        for _, script in install_scripts():
            with self.subTest(script=script.parent.name):
                self.assertIn(
                    "-o pipefail", script.read_text(),
                    f"{script} lacks 'set -o pipefail'",
                )

    def test_every_script_parses_with_nounset(self):
        # `set -u` catches an unset variable at runtime, but an unbound
        # positional parameter is a *parse-time* error, so the existing
        # `bash -n` suite cannot see it. Without -u, `$1` in a recipe that is
        # invoked with no arguments silently expands to empty and the script
        # downloads into the wrong place.
        for _, script in install_scripts():
            result = subprocess.run(
                ["bash", "-u", "-n", str(script)],
                capture_output=True, text=True,
            )
            with self.subTest(script=script.parent.name):
                self.assertEqual(result.returncode, 0,
                                 f"{script}: {result.stderr.strip()}")

    def test_every_script_sets_nounset(self):
        # Without -u, an unset VERSION referenced from a URL line expands to
        # empty and fetches a malformed path, which is how six recipes ended up
        # requesting ".../sources/atk//atk-2.52.0.tar.gz".
        for _, script in install_scripts():
            with self.subTest(script=script.parent.name):
                self.assertIn(
                    "-u", script.read_text().splitlines()[1],
                    f"{script} does not enable 'set -u'",
                )


class TestUrlMatchesRecipeUrl(unittest.TestCase):
    """The download URL must agree with the recipe's own recipe_url field.

    library.toml records the URL independently of install.sh, so the two can
    be compared without either being the authority. Six recipes once
    interpolated an unset VERSION into their URL, producing a request that
    expanded to a different path than the one declared here — the field stayed
    correct, which is exactly what makes this check possible.

    All recipes are expanded in a single bash process: spawning one per recipe
    cost 27 seconds, which is most of the suite's runtime and would grow with
    the recipe count.

    This executes repository-controlled text for real, so it is a trust
    boundary like probe_tar_line: the header lines are run as shell. The
    scripts are repo content, so the risk is a compromised repository rather
    than an external input, but the boundary is worth stating.
    """

    @classmethod
    def setUpClass(cls):
        programs = []
        for _, script in install_scripts():
            assignments = header_assignments(script)
            # A subshell per recipe keeps one script's variables from leaking
            # into the next. ${URL-} reads the value without tripping -u when a
            # git-based recipe declares none.
            programs.append(
                "(\n" + "\n".join(assignments)
                + f'\nprintf "%s\\t%s\\n" "{script}" "${{URL-}}")'
            )

        result = subprocess.run(
            ["bash", "-c", "\n".join(programs)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise AssertionError(f"expanding recipe headers failed: "
                                 f"{result.stderr.strip()}")

        cls.expanded = {}
        for line in result.stdout.splitlines():
            name, _, url = line.partition("\t")
            cls.expanded[Path(name).parent.name] = url

    def expanded_url(self, recipe: str) -> str:
        return self.expanded.get(recipe, "")

    def test_no_positional_expansion_without_a_default(self):
        # $1, $@ and $* need a :- default under -u. All 53 recipes that accept
        # an argument already spell it SCRATCH="${1:-name}".
        positional = re.compile(r'(?<!\$\{)(?<!\$\{1)\$[1-9@*]')
        for _, script in install_scripts():
            for lineno, line in enumerate(script.read_text().splitlines(), 1):
                if line.lstrip().startswith("#"):
                    continue
                with self.subTest(script=script.parent.name, line=lineno):
                    self.assertIsNone(
                        positional.search(line),
                        f"{script}:{lineno}: positional expansion without a "
                        f"default, would abort under 'set -u': {line!r}",
                    )

    def test_every_url_matches_its_recipe_url_field(self):
        mismatches = []
        for toml_file, script in install_scripts():
            declared = load_recipe(toml_file).get("recipe_url", "")
            actual = self.expanded_url(script.parent.name)
            if actual and actual != declared:
                mismatches.append(f"{script}: {actual} != {declared}")
        self.assertEqual(mismatches, [], "\n".join(mismatches))

    def test_expanded_url_is_non_empty_and_absolute(self):
        # A URL that expanded to nothing, or to a relative path, means an
        # unset or malformed variable reached the download step.
        for _, script in install_scripts():
            url = self.expanded_url(script.parent.name)
            if not url:
                continue  # git-based recipe: no URL line
            with self.subTest(script=script.parent.name):
                self.assertTrue(
                    url.startswith("https://"),
                    f"{script}: URL expanded to {url!r}",
                )


class TestDownloadSafety(unittest.TestCase):
    """These scripts are published for users to fetch and run.

    They download an archive over the network and execute code from it, so the
    extraction step is the trust boundary.

    A predictable download path is the defect these guard: every script used to
    `cd /tmp` and `wget` a file named after the version. /tmp is world-writable
    and sticky, so any local user can pre-create that name as a symlink and
    decide what gets extracted and run.
    """

    def test_no_script_downloads_into_a_shared_directory(self):
        for _, script in install_scripts():
            with self.subTest(script=script.parent.name):
                self.assertNotIn(
                    "cd /tmp", script.read_text(),
                    f"{script} downloads into world-writable /tmp",
                )

    def test_every_script_uses_a_private_scratch_directory(self):
        for _, script in install_scripts():
            with self.subTest(script=script.parent.name):
                self.assertIn(
                    "mktemp -d", script.read_text(),
                    f"{script} has no private scratch directory",
                )

    def test_scratch_directory_is_removed_on_exit(self):
        for _, script in install_scripts():
            text = script.read_text()
            if "mktemp -d" not in text:
                continue  # covered by the test above
            with self.subTest(script=script.parent.name):
                self.assertRegex(text, re.compile(r"trap .* EXIT"))

    def test_extraction_does_not_restore_ownership(self):
        # An archive that records uid/gid would otherwise create root-owned
        # files when a recipe is run under sudo.
        for _, script in install_scripts():
            for line in script.read_text().splitlines():
                if not re.match(r"^\s*tar\s", line):
                    continue
                with self.subTest(script=script.parent.name, line=line):
                    self.assertIn("--no-same-owner", line)

    def test_tar_options_follow_the_operation_flag(self):
        # GNU tar rejects `tar --no-same-owner xzf archive` outright: a long
        # option ahead of the clustered operation flag makes it report "You must
        # specify one of the '-Acdtrux' ... options" and extract nothing. That
        # failure is invisible to `bash -n`, so the ordering is pinned here as
        # well as exercised end to end below.
        #
        # The boundary is the *operation*, not the first token: a long option
        # that names an operation (`tar --extract --file ... --no-same-owner`)
        # is legal in any position, so matching any leading `--` would
        # false-positive on a form that works. The authoritative check is the
        # real-archive probe below; this one exists to give a readable diff.
        #
        # Every tar line is checked, not only the ones carrying a particular
        # flag: the rule holds for all of them, and filtering by flag would let
        # dropping that flag from a recipe silently end this check.
        for script, lineno, line, _ in tar_invocations():
            with self.subTest(script=script.parent.name, line=lineno):
                tokens = shlex.split(line)[1:]
                boundary = tar_operation_index(tokens)
                self.assertGreater(
                    boundary, -1,
                    f"{script}:{lineno}: no tar operation flag: {line!r}",
                )
                premature = [
                    token for token in tokens[:boundary]
                    if token.startswith("--") and token not in TAR_OPERATION_LONG
                ]
                self.assertEqual(
                    premature, [],
                    f"{script}:{lineno}: long option precedes the tar "
                    f"operation flag, which GNU tar rejects: {line!r}",
                )

    def test_tar_options_follow_the_archive_operand(self):
        # The other wrong form: `tar xzf --no-same-owner "$ARCHIVE"` makes -f
        # consume --no-same-owner as the archive name, so tar reports that it
        # "Cannot open" that path. A different failure, with a different
        # message, from the one above — which is exactly why a check keyed to
        # one of tar's strings guarded only one of them.
        for script, lineno, line, _ in tar_invocations():
            tokens = shlex.split(line)[1:]
            with self.subTest(script=script.parent.name, line=lineno):
                for index, token in enumerate(tokens[:-1]):
                    if "f" not in short_cluster(token):
                        continue
                    following = tokens[index + 1]
                    self.assertFalse(
                        following.startswith("--"),
                        f"{script}:{lineno}: -f consumes the following "
                        f"token as the archive name: {line!r}",
                    )

    def test_recipes_with_tar_are_executable_end_to_end(self):
        # tar itself as the oracle: run every recipe's tar line as written,
        # against a probe archive built on the spot, and require exit 0.
        #
        # Exit status rather than a grep for tar's wording, because the two
        # wrong argument orders fail differently -- one reports a missing
        # operation flag, the other tries to open "--no-same-owner" as a file.
        # Matching either message left the other unguarded.
        if shutil.which("tar") is None:
            self.skipTest("tar is not installed")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            try:
                archives = probe_archives(root)
            except RuntimeError as exc:
                self.skipTest(str(exc))

            for script, lineno, line, cluster in tar_invocations():
                with self.subTest(script=script.parent.name, line=lineno):
                    result, target = probe_tar_line(
                        root, archives, line, cluster,
                        f"{script.parent.name}-{lineno}")
                    self.assertEqual(
                        result.returncode, 0,
                        f"{script}:{lineno}: tar rejects this command line: "
                        f"{result.args}\n{result.stderr.strip()}",
                    )
                    self.assertTrue(
                        any(target.iterdir()),
                        f"{script}:{lineno}: tar succeeded but extracted "
                        f"nothing into {target}",
                    )


class TestTarProbeSandbox(unittest.TestCase):
    """The probe runs repository text against a real tar, so it is contained.

    This suite executes every recipe's tar line as written. Without a boundary
    that is a test which writes wherever the command line says: a literal `-C`
    would have the probe create and fill a directory outside the temp root, and
    a line with no `-C` at all would extract into the current working
    directory -- the repository.
    """

    def setUp(self):
        if shutil.which("tar") is None:
            self.skipTest("tar is not installed")
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        try:
            self.archives = probe_archives(self.root)
        except RuntimeError as exc:
            self.skipTest(str(exc))

    def probe(self, line):
        return probe_tar_line(self.root, self.archives, line, "xzf", "case")

    def test_a_line_without_dash_c_does_not_write_into_the_repository(self):
        before = set(Path.cwd().iterdir())
        result, extracted = self.probe('tar xzf "$ARCHIVE"')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(any(extracted.iterdir()))
        self.assertEqual(set(Path.cwd().iterdir()), before,
                         "the probe wrote into the repository")

    def test_a_literal_directory_outside_the_probe_is_refused(self):
        # The escape path is unique per run, like the dotdot test below, so a
        # stale directory from a previous buggy run cannot make this fail for
        # the wrong reason.
        outside = self.root.parent / f"escaped-{self.root.name}"
        with self.assertRaisesRegex(AssertionError, "outside the probe"):
            self.probe(f'tar xzf "$ARCHIVE" -C "{outside}"')
        self.assertFalse(outside.exists())

    def test_a_literal_long_form_directory_outside_the_probe_is_refused(self):
        outside = self.root.parent / f"escaped-{self.root.name}"
        with self.assertRaisesRegex(AssertionError, "outside the probe"):
            self.probe(f'tar xzf "$ARCHIVE" --directory="{outside}"')
        self.assertFalse(outside.exists())

    def test_a_recipe_directory_variable_is_accepted(self):
        # The form every recipe actually uses must keep working: the variable
        # resolves to the probe's own target directory.
        result, extracted = self.probe(
            'tar xzf "$ARCHIVE" --no-same-owner -C "$PREFIX"')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(any(extracted.iterdir()))

    def test_a_dotdot_operand_that_resolves_outside_is_refused(self):
        # The lexical is_relative_to check passes for "$PREFIX/../../escaped"
        # because the variable resolves to a path inside the probe; only
        # resolving the .. reveals the escape. The escape path is unique per
        # run so a previous buggy run cannot have left it behind.
        outside = self.root.parent / f"escaped-{self.root.name}"
        with self.assertRaisesRegex(AssertionError, "outside the probe"):
            self.probe(f'tar xzf "$ARCHIVE" -C "$PREFIX/../../{outside.name}"')
        self.assertFalse(outside.exists())


class TestQuoting(unittest.TestCase):
    def test_no_unquoted_prefix_globs(self):
        # cd "$PREFIX"/* is the old unsafe form: it breaks when PREFIX holds
        # more than one entry or contains a space.
        for _, script in install_scripts():
            text = script.read_text()
            self.assertNotIn('cd "$PREFIX"/*\n', text, script)

    def test_cd_globs_are_confined_and_directory_only(self):
        for _, script in install_scripts():
            for line in script.read_text().splitlines():
                if line.startswith("cd ") and "*" in line:
                    with self.subTest(script=script.name, line=line):
                        self.assertRegex(line, SAFE_CD_GLOB)

    def test_expansions_are_quoted(self):
        for _, script in install_scripts():
            for lineno, line in enumerate(script.read_text().splitlines(), 1):
                bare = unquoted_expansions(line)
                self.assertEqual(
                    bare, [],
                    f"{script}:{lineno}: unquoted {', '.join(bare)} in {line!r}")


class TestUnquotedExpansionDetection(unittest.TestCase):
    """The detector itself, so a tightened lint cannot regress to a no-op."""

    def test_bare_expansion_is_flagged(self):
        self.assertEqual(unquoted_expansions("echo $HOME"), ["$HOME"])
        self.assertEqual(unquoted_expansions("cd $PREFIX/src"), ["$PREFIX"])

    def test_expansion_inside_double_quotes_is_clean(self):
        self.assertEqual(unquoted_expansions('cd "$PREFIX/argtable3-${VERSION}"'), [])
        self.assertEqual(unquoted_expansions('mkdir -p "$PREFIX/src"'), [])

    def test_expansion_inside_single_quotes_is_clean(self):
        self.assertEqual(unquoted_expansions("echo '$HOME'"), [])

    def test_expansion_in_command_substitution_is_clean(self):
        # The regression that motivated stripping: the inner "$URL" belongs to
        # a substitution that is itself inside double quotes.
        self.assertEqual(unquoted_expansions('ARCHIVE="$(basename "$URL")"'), [])
        self.assertEqual(unquoted_expansions('make -j$(nproc)'), [])

    def test_expansion_in_nested_parameter_substitution_is_clean(self):
        self.assertEqual(
            unquoted_expansions('COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"'), []
        )

    def test_assignment_rhs_is_clean(self):
        self.assertEqual(unquoted_expansions("PREFIX=$COFFEE/$PACKAGE"), [])
        self.assertEqual(unquoted_expansions("export PATH=$PATH:/opt/bin"), [])

    def test_equals_sign_mid_line_does_not_exempt(self):
        # The old rule matched ".*=" anywhere, so a command whose argument
        # contained an unquoted expansion slipped through.
        self.assertEqual(
            unquoted_expansions('cmake -DFOO=$BAR "$PREFIX"'),
            ["$BAR"],
        )

    def test_comment_is_ignored(self):
        self.assertEqual(unquoted_expansions("# uses $HOME"), [])

    def test_unquoted_braced_expansion_is_flagged(self):
        # ${VAR} is a parameter expansion, not a substitution: unquoted it
        # word-splits exactly like $VAR and must be flagged the same way.
        self.assertEqual(unquoted_expansions("cd ${PREFIX}/src"), ["${PREFIX}"])

    def test_braced_expansion_inside_double_quotes_is_clean(self):
        self.assertEqual(unquoted_expansions('cd "${PREFIX}/src"'), [])


class TestTarArgumentParsing(unittest.TestCase):
    """The tar line analysers, so a guard cannot quietly degrade to a no-op."""

    def test_operation_index_finds_a_short_cluster(self):
        self.assertEqual(
            tar_operation_index(["xzf", "$ARCHIVE", "--no-same-owner"]), 0)

    def test_operation_index_finds_a_long_operation_option(self):
        # The form a valid script may use, and the one a naive "does this line
        # start with --" rule would wrongly reject.
        self.assertEqual(
            tar_operation_index(
                ["--extract", "--file", "a.tar.gz", "--no-same-owner"]), 0)

    def test_operation_index_skips_leading_modifier_options(self):
        self.assertEqual(
            tar_operation_index(["--no-same-owner", "xzf", "a.tar.gz"]), 1)

    def test_operation_index_is_minus_one_without_an_operation(self):
        self.assertEqual(tar_operation_index(["--file", "a.tar.gz"]), -1)

    def test_short_cluster_reads_flags_with_or_without_a_dash(self):
        self.assertEqual(short_cluster("xzf"), "xzf")
        self.assertEqual(short_cluster("-xzf"), "xzf")

    def test_short_cluster_rejects_operands_and_long_options(self):
        for token in ("$ARCHIVE", "/tmp/probe.tar.gz", "--no-same-owner",
                      "--extract", ""):
            with self.subTest(token=token):
                self.assertEqual(short_cluster(token), "")

    def test_short_cluster_accepts_a_single_short_option(self):
        # -C is a short option, not an operand, and must read as one.
        self.assertEqual(short_cluster("-C"), "C")

    def test_compressor_flag_reads_the_cluster(self):
        for cluster, expected in (("xzf", "z"), ("xjf", "j"), ("xJf", "J"),
                                  ("xf", None)):
            with self.subTest(cluster=cluster):
                self.assertEqual(compressor_flag(cluster), expected)

    def test_operation_index_ignores_an_operand_that_looks_like_a_cluster(self):
        # "src" is all letters, so short_cluster reads it as a cluster and 'c'
        # is an operation letter; but it is an operand, not the operation.
        self.assertEqual(
            tar_operation_index(["--file", "a.tar.gz", "src"]), -1)

    def test_directory_operands_tolerates_a_trailing_dash_c(self):
        self.assertEqual(directory_operands(["-C"]), [])

    def test_every_form_the_recipes_use_has_a_probe_archive(self):
        # If a recipe starts using a compressor the probe cannot build, the
        # probe must fail loudly rather than fall back to a wrong archive.
        used = {compressor_flag(cluster) or ""
                for _, _, _, cluster in tar_invocations()}
        self.assertTrue(used, "no tar invocations found")
        for flag in used:
            self.assertIn(flag, TAR_SUFFIX, f"no suffix for {flag!r}")
            self.assertIn(flag, TAR_CREATE, f"no create flag for {flag!r}")


class TestHeaderAssignments(unittest.TestCase):
    """The header extractor itself: both suites run the result as shell.

    Getting this wrong is not a lint miss but an actual side effect, so the
    stop rule is pinned here rather than left to the two callers to agree on.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)

    def script(self, body: str) -> Path:
        path = Path(self._tmp.name) / "install.sh"
        path.write_text(body)
        return path

    def test_collects_assignments_and_skips_shebang_and_set(self):
        header = header_assignments(self.script(
            "#!/bin/bash\n"
            "set -e -o pipefail -u\n"
            "\n"
            'PACKAGE="fixture"\n'
            'VERSION="1.0.0"\n'
            'URL="https://example.invalid/f-$VERSION.tar.gz"\n'
        ))
        self.assertEqual(header, [
            'PACKAGE="fixture"',
            'VERSION="1.0.0"',
            'URL="https://example.invalid/f-$VERSION.tar.gz"',
        ])

    def test_stops_before_archiving(self):
        header = header_assignments(self.script(
            'PACKAGE="fixture"\n'
            'VERSION="1.0.0"\n'
            'ARCHIVE="$(basename "$URL")"\n'
            'WORK="$(mktemp -d)"\n'
        ))
        self.assertNotIn('ARCHIVE="$(basename "$URL")"', header)

    def test_stops_before_the_scratch_directory_without_an_archive_line(self):
        # The five git-clone recipes have no ARCHIVE= line to stop at, so the
        # old loop ran every assignment to the end of the file and executed
        # mktemp -d for real, leaking a temp directory per run.
        header = header_assignments(self.script(
            "#!/bin/bash\n"
            "set -e -o pipefail -u\n"
            "\n"
            'PACKAGE="cjson"\n'
            'GITURL="https://github.com/DaveGamble/cJSON.git"\n'
            'VERSION="1.7.18"\n'
            'BRANCH="v1.7.18"\n'
            "\n"
            'COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"\n'
            'PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"\n'
            'WORK="$(mktemp -d)"\n'
            "trap 'rm -rf \"$WORK\"' EXIT\n"
        ))
        self.assertIn('PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"', header)
        self.assertNotIn("mktemp", "\n".join(header))

    def test_non_assignment_lines_are_not_collected(self):
        header = header_assignments(self.script(
            'PACKAGE="fixture"\n'
            'mkdir -p "$PREFIX"\n'
            'VERSION="1.0.0"\n'
        ))
        self.assertEqual(header, ['PACKAGE="fixture"', 'VERSION="1.0.0"'])

    def test_every_real_script_yields_only_pure_assignments(self):
        for _, script in install_scripts():
            with self.subTest(script=script.parent.name):
                header = header_assignments(script)
                # Non-empty, or this loop below passes vacuously and both
                # callers silently expand nothing -- which is how a broken
                # header would leave three other checks green.
                self.assertTrue(
                    header,
                    f"{script}: header_assignments() found no assignments",
                )
                for line in header:
                    self.assertRegex(line, ASSIGNMENT)

    def test_an_exported_stop_assignment_still_stops(self):
        # ASSIGNMENT tolerates a leading `export`, so STOP_LINES must too:
        # otherwise `export WORK="$(mktemp -d)"` would run and leak a directory.
        header = header_assignments(self.script(
            'PACKAGE="fixture"\n'
            'export WORK="$(mktemp -d)"\n'
            'VERSION="9.9.9"\n'
        ))
        self.assertEqual(header, ['PACKAGE="fixture"'])


class TestDeclaredDependencies(unittest.TestCase):
    # A build command and the host tool it needs declared.
    BUILD_COMMANDS = {
        r"^\./autogen\.sh$": "automake",
        r"^\./autoreconf\b": "autoconf",
        r"^\bautoreconf\b": "autoconf",
        r"^\bcmake\b": "cmake",
        r"^\bmeson\b": "meson",
        r"^\bninja\b": "ninja",
    }

    def build_tools_used(self, text):
        """Return host tools an install.sh invokes that should be declared."""
        return {tool for pattern, tool in self.BUILD_COMMANDS.items()
                if re.search(pattern, text, re.M)}

    def test_build_tools_are_declared_or_host_provided(self):
        for toml_file, script in install_scripts():
            used = self.build_tools_used(script.read_text())
            declared = set(load_recipe(toml_file).get("dependencies") or {})
            for tool in sorted(used):
                with self.subTest(script=script.parent.name, tool=tool):
                    self.assertTrue(
                        tool in declared or tool in HOST_TOOLS,
                        f"{script} runs a {tool} build but does not declare it",
                    )

    def fetch_only_with_build_deps(self):
        """Return the fetch-only recipes that declare unused build tools."""
        offenders = {}
        for toml_file, script in install_scripts():
            text = script.read_text()
            if self.build_tools_used(text) or re.search(r"^make$", text, re.M):
                continue
            declared = set(load_recipe(toml_file).get("dependencies") or {})
            if declared & HOST_TOOLS:
                offenders[script.parent.name] = declared & HOST_TOOLS
        return offenders

    def test_fetch_only_scripts_declare_no_build_tools(self):
        # A script that only downloads must not advertise build dependencies it
        # never uses, which is what made the GnuTLS recipe look buildable.
        for recipe, tools in sorted(self.fetch_only_with_build_deps().items()):
            if recipe in EXPECTED_FETCH_ONLY_WITH_BUILD_DEPS:
                continue
            with self.subTest(script=recipe):
                self.fail(
                    f"{recipe} fetches only but declares {sorted(tools)}; add "
                    f"it to EXPECTED_FETCH_ONLY_WITH_BUILD_DEPS only if the "
                    f"script is genuinely unfinished"
                )

    def test_fetch_only_debt_matches_the_enumerated_set(self):
        # The inversion: the debt is asserted rather than skipped, so neither a
        # fix nor a new offender passes unnoticed.
        self.assertEqual(
            set(self.fetch_only_with_build_deps()),
            set(EXPECTED_FETCH_ONLY_WITH_BUILD_DEPS),
        )


class TestVersions(unittest.TestCase):
    def test_versions_are_not_branch_names(self):
        for toml_file in recipe_files(RECIPES_DIR):
            version = load_recipe(toml_file).get("version", "")
            with self.subTest(recipe=toml_file.parent.name):
                self.assertNotIn(version.strip().lower(), BRANCH_NAMES)

    def test_versions_are_non_empty(self):
        for toml_file in recipe_files(RECIPES_DIR):
            with self.subTest(recipe=toml_file.parent.name):
                self.assertTrue(load_recipe(toml_file).get("version", ""))


class TestSharedLibraries(unittest.TestCase):
    """Static-only libraries cannot be linked by their consumers.

    Autotools' ./configure already defaults to shared libraries, so only the
    hand-rolled configure scripts need the flag spelled out.
    """

    def test_x264_enables_shared(self):
        x264 = RECIPES_DIR / "x" / "x264" / "install.sh"
        if not x264.exists():
            self.skipTest("recipes/x/x264/install.sh moved or was removed")
        text = x264.read_text()
        self.assertIn("--enable-shared", text)
        self.assertIn("--enable-pic", text)
        self.assertNotIn("--disable-shared", text)

    def test_libsais_enables_shared(self):
        # libsais' CMakeLists defaults LIBSAIS_BUILD_SHARED_LIB to OFF.
        libsais = RECIPES_DIR / "l" / "libsais" / "install.sh"
        self.assertTrue(libsais.exists(), "recipes/l/libsais/install.sh missing")
        self.assertIn("-DLIBSAIS_BUILD_SHARED_LIB=ON", libsais.read_text())

    def test_argparse_installs_header_and_shared_library(self):
        # argparse's Makefile has no install target, so the script copies the
        # artifacts itself.
        argparse = RECIPES_DIR / "a" / "argparse" / "install.sh"
        self.assertTrue(argparse.exists(), "recipes/a/argparse/install.sh missing")
        text = argparse.read_text()
        self.assertIn("argparse.h", text)
        self.assertIn("libargparse.so", text)

    def test_wuffs_installs_single_file_library(self):
        # wuffs ships as one amalgamated C file with no build system for C
        # users, so the script copies it into include/.
        wuffs = RECIPES_DIR / "w" / "wuffs" / "install.sh"
        self.assertTrue(wuffs.exists(), "recipes/w/wuffs/install.sh missing")
        text = wuffs.read_text()
        self.assertIn("release/c/wuffs-v0.3.c", text)
        self.assertIn('"$PREFIX/include"', text)

    def test_static_by_default_set_is_exactly_x264(self):
        # A second static-only recipe must be handled explicitly instead of
        # being skipped by the guard below.
        self.assertEqual(EXPECTED_STATIC_BY_DEFAULT, frozenset({"x264"}))

    def test_no_recipe_disables_shared_libraries(self):
        for toml_file, script in install_scripts():
            recipe = script.parent.name
            if recipe in EXPECTED_STATIC_BY_DEFAULT:
                continue
            with self.subTest(script=recipe):
                self.assertNotIn(
                    "--disable-shared", script.read_text(),
                    f"{script} disables shared libraries",
                )


class TestGitCloneDestinationPattern(unittest.TestCase):
    """The lint pattern itself, so it cannot quietly stop matching."""

    def test_plain_clone_matches(self):
        self.assertRegex(
            'git clone --depth 1 --branch "$BRANCH" "$GITURL" "$PACKAGE"',
            GIT_CLONE_WITH_DEST,
        )

    def test_clone_with_trailing_comment_matches(self):
        self.assertRegex(
            'git clone "$GITURL" "$PACKAGE"  # upstream basename differs',
            GIT_CLONE_WITH_DEST,
        )

    def test_clone_without_destination_does_not_match(self):
        self.assertNotRegex(
            'git clone --depth 1 --branch "$BRANCH" "$GITURL"',
            GIT_CLONE_WITH_DEST,
        )

    def test_commented_out_clone_does_not_match(self):
        # A commented-out clone is not a clone: the real-tree guard must not
        # pass a script whose only clone line is disabled.
        self.assertNotRegex(
            '# git clone "$GITURL" "$PACKAGE"',
            GIT_CLONE_WITH_DEST,
        )

    def test_clone_without_destination_but_later_package_use_does_not_match(self):
        # The destination must be the clone's own argument: a "$PACKAGE" in a
        # chained command is not a destination.
        self.assertNotRegex(
            'git clone "$GITURL" && mv checkout "$PACKAGE"',
            GIT_CLONE_WITH_DEST,
        )

    def test_clone_in_a_command_chain_matches(self):
        self.assertRegex(
            'cd "$WORK" && git clone "$GITURL" "$PACKAGE"',
            GIT_CLONE_WITH_DEST,
        )

    def test_clone_with_a_trailing_command_matches(self):
        self.assertRegex(
            'git clone "$GITURL" "$PACKAGE" && cd "$PACKAGE"',
            GIT_CLONE_WITH_DEST,
        )

    def test_indented_clone_matches(self):
        self.assertRegex(
            '  git clone "$GITURL" "$PACKAGE"',
            GIT_CLONE_WITH_DEST,
        )

    def test_clone_followed_by_semicolon_matches(self):
        self.assertRegex(
            'git clone "$GITURL" "$PACKAGE"; cd "$PACKAGE"',
            GIT_CLONE_WITH_DEST,
        )

    def test_clone_after_semicolon_matches(self):
        self.assertRegex(
            'cd "$WORK"; git clone "$GITURL" "$PACKAGE"',
            GIT_CLONE_WITH_DEST,
        )

    def test_clone_after_or_operator_matches(self):
        self.assertRegex(
            'cd "$WORK" || git clone "$GITURL" "$PACKAGE"',
            GIT_CLONE_WITH_DEST,
        )

    def test_clone_in_a_subshell_matches(self):
        self.assertRegex(
            '(cd "$WORK" && git clone "$GITURL" "$PACKAGE")',
            GIT_CLONE_WITH_DEST,
        )

    # Regression pin: green on arrival, not red-first. Guards the pipe in the
    # trailing lookahead.
    def test_clone_piped_matches(self):
        self.assertRegex(
            'git clone "$GITURL" "$PACKAGE" | tee log',
            GIT_CLONE_WITH_DEST,
        )

    def test_clone_destination_used_as_path_prefix_matches(self):
        self.assertRegex(
            'git clone "$GITURL" "$PACKAGE"/sub',
            GIT_CLONE_WITH_DEST,
        )

    # Regression pin: green on arrival, not red-first. Guards the leading-# /
    # indentation interaction with the command-position anchor.
    def test_indented_commented_out_clone_does_not_match(self):
        self.assertNotRegex(
            '  # git clone "$GITURL" "$PACKAGE"',
            GIT_CLONE_WITH_DEST,
        )


class TestRealRepository(unittest.TestCase):
    def test_every_recipe_has_an_install_script(self):
        for toml_file in recipe_files(RECIPES_DIR):
            with self.subTest(recipe=toml_file.parent.name):
                self.assertTrue((toml_file.parent / "install.sh").exists())

    def test_git_clone_names_an_explicit_destination(self):
        # git clone without a destination checks out into the upstream repo's
        # basename (cJSON, WavPack), which need not match $PACKAGE; the
        # following `mv "$PACKAGE" "$PREFIX"` then fails on a case-sensitive
        # filesystem after rm -rf already destroyed the previous install.
        for toml_file, script in install_scripts():
            for lineno, line in enumerate(script.read_text().splitlines(), 1):
                if "git clone" not in line:
                    continue
                with self.subTest(script=script.parent.name, line=lineno):
                    self.assertRegex(
                        line, GIT_CLONE_WITH_DEST,
                        f"{script}:{lineno} clones without an explicit "
                        f"destination",
                    )


if __name__ == "__main__":
    unittest.main()
