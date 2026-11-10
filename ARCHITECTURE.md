# Architecture

How this repository turns recipe metadata into a published site.

## Directory layout

- `recipes/<letter>/<name>/` — the source of truth. Each recipe is
  `library.toml` (metadata) plus `install.sh` (a template; the site serves it
  with a header rendered from `library.toml`).
  The letter bucket is a routing convenience only; see *Naming* below.
- `recipe_metadata.py` — shared vocabulary. Recipe discovery, letter routing,
  TOML loading, name aliasing, dependency normalization, last-updated dates.
  Every checker and generator imports from here.
- `check_canonical_names.py` — canonical names must be unique and usable as a
  C identifier prefix.
- `check_toml_schema.py` — required fields present and well typed.
- `check_dependencies.py` — every `[dependencies]` entry resolves to a recipe
  and every `[build-dependencies]` entry to an accepted host tool.
- `generate_mdbook_src.py` — recipes to Markdown in `src/`.
- `generate_packages.py` — recipes to JSON in `docs/`.
- `recipe_script.py` — renders a published install.sh from its template, and
  reads the pure leading assignments of a rendered one.
- `test_*.py` — one module per checker plus shared-helper and generator tests.
- `Makefile` — `all` (checks + site), `site` (build only), `clean`.

## Data flow

```
recipes/*/*/library.toml
        |
        +-- recipe_metadata.py -- shared parsing, name aliasing, dates
        |
        +-> check_canonical_names.py  --+
        +-> check_toml_schema.py       +-- exit non-zero on any finding
        +-> check_dependencies.py     --+
        |
        +-> generate_mdbook_src.py --> src/*.md + rendered install.sh
        |                                 |
        |                                 +-> mdbook build --> docs/*.html
        |
        +-> generate_packages.py ----> docs/<letter>/<dir>/<Title>.json
                                      docs/.well-known/packages.json
```

`mdbook build` is the only external tool in the pipeline. Everything else is
stdlib Python; nothing here has a third-party dependency.

## Naming

A recipe answers to two names, both derived from its path and metadata:

- `canonical_name` — underscored, valid C identifier, unique. Becomes the
  prefix for generated variables and functions downstream.
- the **directory name** — may keep the upstream dashed spelling
  (`recipes/j/json-c/`, `recipes/l/libjpeg-turbo/`). Registered as an alias, so
  dependencies may use either spelling.

Dependency resolution is exact-match against those names. It
does not rewrite dashes to underscores: that rewrite silently failed for the
renames it was added for, and the directory alias already covers the real
cases.

## Trust boundaries

Two places where a bug produces a *false green*, both guarded by explicit
refusals rather than by accident:

- **Empty tree.** Every checker refuses to report success when it finds no
  recipes. A checker that passes because it looked in the wrong place is worse
  than one that crashes. This is why the checkers use `RECIPES_DIR` (absolute)
  and not a relative `Path("recipes")`.
- **`HOST_TOOLS`** (`check_dependencies.py`) — build and host tooling assumed to
  exist rather than be built from a recipe. Only `[build-dependencies]` may name
  these, and `[dependencies]` may not: coffee fetches the latter from the
  registry, and there is no cmake recipe to fetch. The list holds only tools
  some script invokes, never a library.

A green `make checks` means *no metadata is malformed and no dependency is a
typo*. It does not mean any recipe builds.

## Data flow: install.sh

These scripts are published for users to fetch and run, which makes the
download step the trust boundary.

The repository holds a *template* per recipe: `#!/bin/bash`,
`set -e -o pipefail -u`, then a body. `recipe_script.render_install_script()`
publishes it with a header generated from `library.toml` that defines
`PACKAGE`, `VERSION`, `URL`, `COFFEE_HOME`, `PREFIX` (`$1`, or
`$COFFEE_HOME/<canonical_name>/<version>`, made absolute) and a scratch
directory `WORK` removed by `trap ... EXIT`, then `cd`s into it. A template that
assigns any of those variables is refused, so `library.toml` stays the single
place that names a version or URL. The values are inserted with `shlex.quote`,
so metadata is data, never shell. The full contract is in README.md.

The enforced shape:

- `set -e -o pipefail -u`. The `-u` is what turns a mis-scoped variable into a
  loud failure: six recipes once assigned `VERSION` *after* the `URL` line that
  interpolated it, and without `-u` each silently fetched a malformed path like
  `.../sources/atk//atk-2.52.0.tar.gz`.
- download into the private `WORK` directory, never a predictable path in
  world-writable `/tmp`
- `tar --no-same-owner` so an archive cannot create root-owned files
- build in `WORK` and install into `$PREFIX`; never unpack sources into the
  prefix, never delete it (it may be a directory the user named, such as
  `/usr/local`), and pin CMake and Meson to `lib` rather than `lib64`
- `meson setup --wrap-mode=nofallback`: otherwise Meson silently substitutes a
  bundled or downloaded copy for a missing dependency. fontconfig's gperf wrap,
  for one, clones an unpinned git branch, which is an unverified download
  outside `$URL`. `--wrap-mode=nodownload` is the one alternative, for a
  release tarball that vendors subprojects with no recipe (criterion): it
  builds them from the tarball and never fetches

The lint suites run on the *rendered* scripts, since those are what users
execute. `test_install_scripts.py::TestInstallContract` checks the templates
themselves: each renders, each has an install step, none unpacks into or
deletes the prefix.

`recipe_script.header_assignments()` owns what "the assignments" means, for
both suites that run them as shell. It stops at `ARCHIVE=` *or* `WORK=`, so the
header's `mktemp -d` is never executed by a test.

GNU tar rejects a long option placed before the clustered operation flag, and
the two wrong orders fail *differently*: `tar --no-same-owner xzf a.tgz` reports
a missing operation, while `tar xzf --no-same-owner a.tgz` has `-f` swallow the
option as the archive name. Matching either message in stderr guarded only one
of them. `test_install_scripts.py` instead builds a real probe archive per
compression form in use and requires exit 0, with a static check per wrong form
alongside for a readable diff. The static boundary is the *operation*, not the
first token, so a working `tar --extract --file ... --no-same-owner` is not
flagged; that check covers every tar line rather than only those carrying a
particular flag, so dropping that flag cannot quietly end it.

Because the probe executes repository-controlled text for real, it is itself
a trust boundary. `probe_tar_line()` runs each line with `cwd` set to a fresh
directory inside the suite's temp root, so a line that omits `-C` extracts
there instead of into the repository, and a `-C` operand naming a literal path
outside that root is refused rather than created. Recipe variables resolve to
the probe's own target, so only a hardcoded path can escape. The `resolve()`
boundary was reviewed and deliberately accepted as-is: a hardcoded path is the
one escape it cannot close, and refusing it is the documented contract.

`test_install_script_execution.py` runs those lines with `TMPDIR` pointed at a
directory the suite owns. Asserting the system temp instead would be vacuous:
`mktemp -d` creates a sibling of the fixture root, so "no `tmp.*` here" holds
whether or not the trap fired. A control test asserts the scratch directory
*survives* with the trap removed, so the cleanup tests cannot go quiet again.

**Download integrity.** `library.toml` carries a required `sha256` and a
`sha256_source`. The generated header downloads `$URL` to `$ARCHIVE` and runs
`sha256sum -c` before any template code, so nothing from an archive is read
unless its digest matches. Templates may not download anything themselves
(`wget`, `curl`, `git clone` are refused at render time), which is why git
recipes were moved to release tarballs: a clone cannot be checksummed.

`sha256_source` records how far the pinned digest is trusted:

- `signature`: the archive's upstream signature was verified with the
  project's key when the digest was recorded
- `upstream`: upstream publishes this sha256 (a `.sha256` file, SHA256SUMS,
  release notes, or GitHub's release-asset digest), and it matched
- `tofu`: nothing upstream to compare with (typically GitHub's generated
  `archive/refs/tags/` tarballs); the digest of a first download is pinned

Signatures are checked once, when a digest is recorded, not at install time:
users need only `sha256sum`. When bumping a version, re-derive the digest from
the strongest source available and update `sha256_source` to match.

## Current state

- Every template builds and installs into the prefix, and every download is
  checked against a pinned sha256. Whether each one builds on a given host
  still depends on that host's toolchain and system libraries, which the
  unit tests cannot see.
- `book.toml` sets `create-missing = false`, so a `SUMMARY.md` entry without a
  corresponding page fails the build rather than silently emitting an empty one.

## Deliberate trade-offs

Recorded here so they are not rediscovered as defects.

- **`--no-same-owner` covers ownership, not traversal.** It stops an archive
  from creating root-owned files when a recipe runs under `sudo`. It does *not*
  address archive path traversal. GNU tar ≥ 1.32 strips `../` and absolute
  members by default, so this holds on a current host, but nothing here pins or
  asserts the user's tar. If that assumption is ever dropped, the lever is an
  explicit `--strip-components` policy per recipe.
- **`.DELETE_ON_ERROR` trades incremental local builds for correctness.** If the
  generator fails partway through, a previously-good `SUMMARY.md` is deleted
  rather than left behind. Republishing a stale table is the worse failure, so
  the Makefile prefers a rebuild over a plausible-looking wrong page.
- **The mdBook tarball digest is trust-on-first-use.** GitHub publishes no
  checksum for the v0.4.36 release, so the SHA-256 in
  `.github/workflows/build.yml` was taken from a first trusted download rather
  than an upstream-published value. That is the issue, not just the fact: a
  compromised first download would pin a malicious digest that every later
  build then verifies against, so the pin is only as good as the machine that
  first fetched it. Mitigations: re-derive the digest when the mdBook version
  changes, review it in PR, and switch to an upstream-published value if one
  ever appears. The trust-on-first-use pin was reviewed and accepted as-is;
  the mitigations above remain the standing policy.
