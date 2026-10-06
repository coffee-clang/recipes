# Architecture

How this repository turns recipe metadata into a published site.

## Directory layout

- `recipes/<letter>/<name>/` — the source of truth. Each recipe is
  `library.toml` (metadata) plus `install.sh` (the script the site serves).
  The letter bucket is a routing convenience only; see *Naming* below.
- `recipe_metadata.py` — shared vocabulary. Recipe discovery, letter routing,
  TOML loading, name aliasing, dependency normalization, last-updated dates.
  Every checker and generator imports from here.
- `check_canonical_names.py` — canonical names must be unique and usable as a
  C identifier prefix.
- `check_toml_schema.py` — required fields present and well typed.
- `check_dependencies.py` — every declared dependency resolves to a recipe or
  an accepted host tool.
- `generate_mdbook_src.py` — recipes to Markdown in `src/`.
- `generate_packages.py` — recipes to JSON in `docs/`.
- `recipe_script.py` — reads the pure leading assignments of an install.sh.
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
        +-> generate_mdbook_src.py --> src/*.md + install.sh
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

Dependency resolution is exact-match against those names plus `HOST_TOOLS`. It
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
  exist rather than be built from a recipe. A trust boundary: anything listed is
  exempt from resolution, so the list holds only tools some script invokes,
  never a library. Adding a library here would let a genuinely missing recipe
  pass silently.

A green `make checks` means *no metadata is malformed and no dependency is a
typo*. It does not mean any recipe builds.

## Data flow: install.sh

These scripts are published for users to fetch and run, which makes the
download step the trust boundary. The enforced shape is:

- `set -e -o pipefail -u`. The `-u` is what turns a mis-scoped variable into a
  loud failure: six recipes assigned `VERSION` *after* the `URL` line that
  interpolated it, and without `-u` each silently fetched a malformed path like
  `.../sources/atk//atk-2.52.0.tar.gz`.
- download into `WORK="$(mktemp -d)"`, removed by `trap ... EXIT` — never a
  predictable path in world-writable `/tmp`
- `tar --no-same-owner` so an archive cannot create root-owned files

A static `bash -n` pass cannot see an unbound variable, so `test_install_scripts.py`
pairs `bash -u -n` with a runtime check: every script's variable assignments are
expanded in a single bash process and the resulting `$URL` compared against the
independently-maintained `recipe_url` field in `library.toml`. Both must agree,
and the URL must be absolute. That check is what would catch a repeat of the
six-recipe bug.

`recipe_script.py` owns what "the assignments" means, for both suites that run
them as shell. It stops at `ARCHIVE=` *or* `WORK=` — the latter matters for the
five git-clone recipes, which have no `ARCHIVE=` line and would otherwise
execute `mktemp -d` for real, leaking a directory per run.

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

**Not yet enforced: download integrity.** No recipe carries a checksum or
signature, so a compromised mirror or upstream yields code execution as the
invoking user. The natural fix is a `sha256` field on `library.toml` verified
with `sha256sum -c` before extraction; it was deferred pending a decision on
sourcing digests from upstream-published checksums rather than pinning whatever
a first download happened to return.

## Current state

- 114 recipes, split roughly 92 fetch-only / 22 that build. Whether fetch-only
  is intentional or an unfinished backlog is an open question; the fetch-only
  recipes that nonetheless declare build tools are enumerated as
  `EXPECTED_FETCH_ONLY_WITH_BUILD_DEPS` in `test_install_scripts.py`.
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
- **Fetch-only is unresolved.** ~92 of 114 scripts download and extract without
  building. This may be intentional staging or an unfinished backlog; the code
  deliberately does not guess.
- **`sha256` verification is absent.** No recipe pins a digest, so a compromised
  upstream still yields code execution as the invoking user. The schema change is
  straightforward; what is missing is a decision on sourcing digests from
  upstream-published checksums rather than pinning whatever a first download
  returned.
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
