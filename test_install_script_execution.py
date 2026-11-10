#!/usr/bin/env python3
"""Execute an install.sh end to end against a local archive.

test_install_scripts.py asserts that the hardening is *present* — that
`mktemp -d`, `trap`, and `--no-same-owner` appear in the text. That cannot show
the hardening *works*. This module runs a real recipe script against a tarball
built on the spot and a `file://` URL, so nothing touches the network, and
observes the effects that matter:

  - the archive lands under the prefix, not in a shared directory
  - the scratch directory is removed when the script exits
  - the scratch directory is also removed when the script *fails*
  - extraction does not take ownership from the archive

The recipe under test is a fixture, not a real library: it follows the same
shape as recipes/l/libffi/install.sh so the shared invariants are what get
exercised.
"""

import hashlib
import os
import re
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

from recipe_metadata import load_recipe
from recipe_script import (
    TEMPLATE_PREAMBLE,
    header_assignments,
    render_install_script,
)

# A template in the same shape as a real recipe: everything above the body
# (prefix, scratch directory, trap) comes from the generated header, so the
# behaviours below exercise the header every published script shares.
FIXTURE_TEMPLATE = TEMPLATE_PREAMBLE + """\
tar xzf "$ARCHIVE" --no-same-owner
mkdir -p "$PREFIX"
cp payload.txt "$PREFIX/"
"""

# wget does not speak file://, and these tests must not reach the network, so a
# shim earlier on PATH serves a local tarball instead. Only the fetch is
# substituted: mktemp, trap, tar --no-same-owner and `set -u` all run for real.
# That wget is invoked with a quoted URL is already covered statically in
# test_install_scripts.py.
WGET_SHIM = """#!/bin/bash
set -e
url=""
out=""
while [ $# -gt 0 ]; do
    case "$1" in
        -O) out="$2"; shift 2 ;;
        -*) shift ;;
        *) url="$1"; shift ;;
    esac
done
case "$url" in
    file://*) src="${url#file://}" ;;
    *) echo "shim: unsupported scheme: $url" >&2; exit 1 ;;
esac
[ -f "$src" ] || { echo "shim: no such file: $src" >&2; exit 8; }
[ -n "$out" ] || out="./$(basename "$src")"
cp "$src" "$out"
"""


def build_fixture_script(url: str) -> str:
    """Render the fixture, pinning the digest of the archive url names.

    A url naming no file gets a digest that matches nothing, which the tests
    for a failed download never reach.
    """
    source = Path(url.removeprefix("file://"))
    digest = (hashlib.sha256(source.read_bytes()).hexdigest()
              if source.is_file() else "0" * 64)
    return render_install_script(FIXTURE_TEMPLATE, {
        "canonical_name": "fixture", "version": "1.0.0", "recipe_url": url,
        "sha256": digest,
    })


def rendered_recipes(directory: Path):
    """Yield (name, path) for every real recipe's published install.sh."""
    from recipe_metadata import RECIPES_DIR, recipe_files

    for toml_file in recipe_files(RECIPES_DIR):
        template = toml_file.parent / "install.sh"
        if not template.exists():
            continue
        path = directory / f"{toml_file.parent.name}.sh"
        path.write_text(render_install_script(template.read_text(),
                                              load_recipe(toml_file)))
        yield toml_file.parent.name, path


def make_tarball(directory: Path, payload: str = "hello",
                 owner: str | None = None) -> Path:
    """Build a .tar.gz containing a single file, and return its path."""
    source = directory / "src"
    source.mkdir()
    (source / "payload.txt").write_text(payload)

    archive = directory / "fixture-1.0.0.tar.gz"
    cmd = ["tar", "--no-same-owner"]
    if owner is not None:
        # Record an ownership the extracting user does not have, so the test can
        # observe whether it was honoured.
        cmd += [f"--owner={owner}", "--group=0", "--numeric-owner"]
    cmd += ["-czf", str(archive), "-C", str(source), "payload.txt"]
    subprocess.run(cmd, check=True, capture_output=True)
    return archive


class InstallScriptExecutionTest(unittest.TestCase):
    def setUp(self):
        if shutil.which("tar") is None:
            self.skipTest("tar is not installed")

        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

        # An isolated COFFEE_HOME so the test never reads or writes the real
        # ~/.coffee.
        self.coffee = self.root / "coffee"
        self.coffee.mkdir()

        # The script's own TMPDIR, inside self.root. Without this, `mktemp -d`
        # creates its scratch directory in the system temp — a sibling of
        # self.root, not a child — so asserting that self.root holds no
        # "tmp.*" would be true whether or not the trap worked.
        self.scratch = self.root / "scratch"
        self.scratch.mkdir()

        # A downloader that serves a local file, placed first on PATH.
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.shim = self.bin / "wget"
        self.shim.write_text(WGET_SHIM)
        self.shim.chmod(0o755)

    def run_script(self, script: Path, **env_extra):
        env = {
            **os.environ,
            "COFFEE_HOME": str(self.coffee),
            "HOME": str(self.coffee),
            "TMPDIR": str(self.scratch),
            "PATH": f"{self.bin}{os.pathsep}{os.environ['PATH']}",
            **env_extra,
        }
        return subprocess.run(
            ["bash", str(script)], capture_output=True, text=True, env=env,
        )

    def install(self):
        """Write and run the unmodified fixture; it is expected to succeed."""
        archive = make_tarball(self.root)
        url = f"file://{archive}"
        script = self.root / "install.sh"
        script.write_text(build_fixture_script(url))

        result = self.run_script(script)
        self.assertEqual(
            result.returncode, 0,
            f"script failed: {result.stderr.strip()}",
        )
        return result, script, url

    def extracted(self):
        return self.coffee / "fixture" / "1.0.0" / "payload.txt"

    # -- the behaviours under test ------------------------------------------

    def test_archive_is_extracted_into_the_prefix(self):
        self.install()
        self.assertTrue(self.extracted().is_file())
        self.assertEqual(self.extracted().read_text(), "hello")

    def test_nothing_is_left_in_the_shared_tmp(self):
        # The defect this guards: every script used to `cd /tmp` and wget a
        # version-named file there, which any local user could pre-create as a
        # symlink. A private scratch directory must leave /tmp alone.
        self.install()
        self.assertFalse(Path("/tmp/fixture-1.0.0.tar.gz").exists())
        self.assertFalse(Path("/tmp/payload.txt").exists())

    def scratch_contents(self):
        """Return what survived in the TMPDIR the script actually used."""
        return list(self.scratch.iterdir())

    def test_scratch_directory_is_removed_on_success(self):
        _, script, _ = self.install()
        leftovers = re.findall(r'WORK="\$\(mktemp -d\)"', script.read_text())
        self.assertTrue(leftovers, "fixture lost its scratch directory")
        # The trap already ran by the time the process exited; nothing from the
        # run may survive in the TMPDIR the script was given.
        self.assertEqual(self.scratch_contents(), [])

    def test_scratch_directory_survives_without_a_trap(self):
        # The control for the two tests above. Without it they could pass
        # vacuously: an assertion against a directory the script never wrote
        # to is empty whether or not the trap works. Removing the trap must
        # make the scratch directory non-empty.
        body = "\n".join(line for line in build_fixture_script(
            f"file://{make_tarball(self.root)}"
        ).splitlines() if not line.startswith("trap ")) + "\n"
        script = self.root / "install.sh"
        script.write_text(body)

        result = self.run_script(script)
        # Asserted so the control cannot pass by aborting before mktemp.
        self.assertEqual(result.returncode, 0,
                         f"control script failed: {result.stderr.strip()}")

        self.assertNotEqual(self.scratch_contents(), [],
                            "trap removed but the scratch directory vanished; "
                            "the cleanup assertions above are vacuous")

    def test_scratch_directory_is_removed_on_failure(self):
        # A failing recipe must not leave a directory behind, or repeated
        # failures fill the filesystem.
        script = self.root / "install.sh"
        script.write_text(build_fixture_script("file:///nonexistent.tar.gz")
                          + "\nexit 3\n")

        result = self.run_script(script)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.scratch_contents(), [])

    def test_extraction_does_not_take_ownership_from_the_archive(self):
        # An archive recording a uid/gid would otherwise create files owned by
        # that id. --no-same-owner means the extracting user owns them.
        archive = make_tarball(self.root, owner="0")

        script = self.root / "install.sh"
        script.write_text(build_fixture_script(f"file://{archive}"))
        self.assertEqual(self.run_script(script).returncode, 0)

        extracted = self.extracted()
        self.assertTrue(extracted.is_file())
        self.assertEqual(extracted.stat().st_uid, os.getuid())

    def test_unset_variable_aborts_the_script(self):
        # The behaviour `set -u` exists to provide: without it, a recipe that
        # referenced $VERSION before assigning it silently downloaded from a
        # malformed URL, which is what six recipes once did.
        archive = make_tarball(self.root)
        body = build_fixture_script(f"file://{archive}").replace(
            'PREFIX="${1:-$COFFEE_HOME/$PACKAGE/$VERSION}"',
            'echo "$UNSET_VAR"',
        )
        script = self.root / "install.sh"
        script.write_text(body)

        result = self.run_script(script)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("UNSET_VAR", result.stderr)

    def test_a_tampered_archive_is_not_extracted(self):
        # The digest is pinned for the original archive; replacing the file
        # behind the URL afterwards must stop the script before tar runs.
        archive = make_tarball(self.root)
        script = self.root / "install.sh"
        script.write_text(build_fixture_script(f"file://{archive}"))
        archive.write_bytes(archive.read_bytes() + b"tampered")

        result = self.run_script(script)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("checksum", result.stderr)
        self.assertFalse(self.extracted().exists())
        self.assertEqual(self.scratch_contents(), [])

    def test_missing_download_fails_rather_than_extracting_nothing(self):
        # `set -e` must stop the script at the failed fetch, not carry on to
        # extract whatever happened to be in the scratch directory.
        script = self.root / "install.sh"
        script.write_text(
            build_fixture_script(f"file://{self.root}/absent-1.0.0.tar.gz")
        )
        result = self.run_script(script)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.extracted().exists())
        self.assertEqual(self.scratch_contents(), [])


class TestRealRecipesAreExecutable(unittest.TestCase):
    """A spot-check that real recipes run, without downloading anything.

    Executing all 114 would mean 114 network fetches, so this checks the part
    that is pure shell: the hardened preamble up to the download command.
    """

    def test_preamble_runs_and_defines_the_expected_variables(self):
        if shutil.which("bash") is None:
            self.skipTest("bash is not installed")

        failures = []
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        for _, script in rendered_recipes(Path(tmp.name)):
            header = header_assignments(script)
            if not header:
                # A recipe with no collectable assignments would otherwise be
                # skipped here while the three checks that expand this header
                # expanded nothing and passed.
                failures.append(f"{script}: no assignments collected")
                continue

            result = subprocess.run(
                ["bash", "-u", "-c",
                 "\n".join(header) + '\nprintf "%s|%s" "${URL-}" "${VERSION-}"'],
                capture_output=True, text=True,
            )
            if result.returncode != 0:
                failures.append(f"{script}: {result.stderr.strip()}")
            elif "|" in result.stdout and not result.stdout.split("|")[1]:
                failures.append(f"{script}: VERSION expanded to empty")

        self.assertEqual(failures, [], "\n".join(failures))

    def test_preamble_invariants_hold_for_recipes_and_fixture(self):
        """What this fixture claims to share with the recipes, asserted.

        Line order is deliberately not asserted: recipes legitimately place
        ARCHIVE= before or after `mkdir -p "$SCRATCH"`, so requiring an exact
        sequence would flag a legitimate variance as drift.
        """
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        sources = [("fixture", build_fixture_script("file:///nonexistent"))]
        sources += [(name, path.read_text())
                    for name, path in rendered_recipes(Path(tmp.name))]

        for name, text in sources:
            lines = text.splitlines()
            with self.subTest(script=name):
                self.assertEqual(lines[0], "#!/bin/bash", name)
                self.assertEqual(lines[1], "set -e -o pipefail -u", name)

                try:
                    work = next(i for i, line in enumerate(lines)
                                if 'WORK="$(mktemp -d)"' in line)
                except StopIteration:
                    self.fail(f"{name}: no scratch directory declared")
                self.assertEqual(
                    lines[work + 1], "trap 'rm -rf \"$WORK\"' EXIT",
                    f"{name}: the trap must immediately follow the mktemp",
                )

                for line in lines:
                    if line.strip().startswith("tar "):
                        self.assertIn("--no-same-owner", line,
                                      f"{name}: {line!r}")

    def test_install_scripts_are_executable_files(self):
        from recipe_metadata import RECIPES_DIR, recipe_files

        for toml_file in recipe_files(RECIPES_DIR):
            script = toml_file.parent / "install.sh"
            if script.exists():
                with self.subTest(script=script.parent.name):
                    self.assertTrue(
                        script.stat().st_mode & stat.S_IXUSR,
                        f"{script} is not executable by its owner",
                    )


if __name__ == "__main__":
    unittest.main()
