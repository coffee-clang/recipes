# recipes
Recipes of all packages

The recipe canonical name must be a valid C identifier, since it will be used as a prefix for all variables and functions.

## Install contract

Each recipe's `install.sh` in this repository is a template. The site publishes
it with a header generated from `library.toml`, so the version and URL live in
one place.

- The published script takes the install prefix as its first argument. Without
  one it uses `$COFFEE_HOME/<canonical_name>/<version>`, with `COFFEE_HOME`
  defaulting to `~/.coffee`. A relative prefix is resolved against the caller's
  working directory.
- The header defines `PACKAGE` (the `canonical_name`), `VERSION`, `URL` (the
  `recipe_url`), `PREFIX`, and a scratch directory `WORK` that is removed on
  exit. The template body starts inside `WORK` and must not assign any of them.
- The header downloads `$URL` to `$ARCHIVE` in the scratch directory and
  checks it against the `sha256` in `library.toml` before anything else runs.
  The template body extracts `$ARCHIVE`, builds, and installs; it may not
  download anything itself. Headers
  end up in `$PREFIX/<include_dir>` and libraries in `$PREFIX/<lib_dir>`
  (`include` and `lib` unless `library.toml` says otherwise). Sources are never
  unpacked into the prefix, and the prefix is never deleted.
- Libraries the build needs are found through the standard variables the
  caller sets (`PKG_CONFIG_PATH`, `CMAKE_PREFIX_PATH`, `CPPFLAGS`, `LDFLAGS`).
- To link against an installed recipe, use `-I$PREFIX/<include_dir>`,
  `-L$PREFIX/<lib_dir>` and `-l<name>` for each `libname`. A `header_only`
  recipe has nothing to link; read its `notes` for any implementation macro.
