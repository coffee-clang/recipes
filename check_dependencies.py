#!/usr/bin/env python3
"""Validate that every recipe dependency names something buildable.

A dependency is satisfied when it matches a recipe's canonical_name, the
recipe directory name, or one of HOST_TOOLS (tools assumed present on the
host toolchain rather than built from source).

This checks NAME RESOLUTION ONLY. A green run does not mean a recipe builds:
it means no dependency points at a typo. Completeness of a recipe's
dependency list (tools or libraries it needs but does not declare) is out of
scope, which is why gaps such as GnuTLS' libtasn1 or libX11's xcb-proto are
invisible here.
"""

import sys
from pathlib import Path

from recipe_metadata import (
    RECIPES_DIR,
    load_recipe,
    recipe_build_dependencies,
    recipe_dependencies,
    recipe_files,
    recipe_names,
)

# Build and host tooling assumed to exist on the toolchain rather than being
# built from a recipe. This is a trust boundary: anything listed here is
# exempt from resolution, so it is deliberately minimal: every entry is a
# tool some recipe invokes in its install.sh, never a library. Adding a
# library here would let a genuinely missing recipe pass silently.
HOST_TOOLS = frozenset({
    "autoconf",
    "automake",
    "bison",
    "cmake",
    "flex",
    "gettext",
    "gfortran",
    "gperf",
    "java",
    "libtool",
    "m4",
    "meson",
    "nasm",
    "ninja",
    "perl",
    "pkg-config",
    "python3",
})


class AliasCollision(Exception):
    """Two recipes answer to the same name, so resolution is ambiguous."""

    def __init__(self, name: str, first: Path, second: Path):
        super().__init__(f"name '{name}' is claimed by both {first} and {second}")
        self.name = name
        self.first = first
        self.second = second


def resolve(dep: str, recipes: dict[str, dict]) -> bool:
    """Return True when dep names a recipe or a host tool, exactly.

    Resolution is by exact name, never by rewriting dashes to underscores. The
    rewrite used to map a renamed dependency's old dashed spelling onto its
    new canonical name, which was a reasonable idea, but it is dead code today
    and it hides mistakes:

    - Dead, because the eight recipes that keep a dashed spelling carry it as
      their *directory* name, which is registered as an alias in its own right.
      All three dashed dependencies in the tree resolve by exact match.
    - Harmful, because it accepts a spelling that matches no real recipe name.
      A dependency written as ``libjpeg-turbo`` against a recipe stored as
      ``jpegdir`` would be reported as resolved when nothing provides it. A typo
      should fail the check, not be quietly normalized into a pass.

    Host tools resolve only from [build-dependencies]; see check_entry.
    """
    return dep in recipes


def check_entry(entry: dict, recipes: dict[str, dict]) -> list[str]:
    """Return the resolution errors for one recipe's two dependency tables.

    [dependencies] names registry libraries, which coffee fetches, so each must
    be a recipe. [build-dependencies] names host tools, which are checked on
    the host and never fetched, so each must be in HOST_TOOLS.
    """
    path = entry["path"]
    errors = []
    for dep in entry["deps"]:
        if dep in entry["names"]:
            errors.append(f"{path}: '{dep}' depends on itself")
        elif dep in HOST_TOOLS:
            errors.append(
                f"{path}: '{dep}' is a host tool; move it to "
                f"[build-dependencies]"
            )
        elif not resolve(dep, recipes):
            errors.append(f"{path}: dependency '{dep}' has no recipe")
    for tool in entry["build_deps"]:
        if tool not in HOST_TOOLS:
            errors.append(
                f"{path}: build dependency '{tool}' is not a known host tool"
            )
    return errors


def collect_entries(base_dir: Path) -> list[dict]:
    """Parse every recipe once into {path, names, deps} records.

    Unlike the schema and canonical-name checkers, this does not
    report-and-continue on a malformed file: the entries feed a shared name
    index, and a recipe that cannot be parsed cannot be indexed, so continuing
    would blame every dependent for a missing recipe. Stopping at the first
    bad file is the honest failure.
    """
    entries = []

    for toml_file in recipe_files(base_dir):
        data = load_recipe(toml_file)
        entries.append({
            "path": toml_file,
            "names": recipe_names(toml_file, data),
            "deps": recipe_dependencies(toml_file, data),
            "build_deps": recipe_build_dependencies(toml_file, data),
        })

    return entries


def index_entries(entries: list[dict]) -> dict[str, dict]:
    """Map every known name to its recipe record.

    Raises AliasCollision if two recipes claim the same name.
    """
    recipes: dict[str, dict] = {}

    for entry in entries:
        for name in entry["names"]:
            existing = recipes.get(name)
            if existing is None:
                recipes[name] = entry
            elif existing["path"] != entry["path"]:
                raise AliasCollision(name, existing["path"], entry["path"])

    return recipes


def collect_recipes(base_dir: Path) -> dict[str, dict]:
    """Map every known name (canonical + directory) to its recipe metadata."""
    return index_entries(collect_entries(base_dir))


def _check_dependencies(base_dir: Path) -> tuple[list[str], int]:
    """Return (errors, count) from a single tree walk."""
    entries = collect_entries(base_dir)
    recipes = index_entries(entries)
    errors: list[str] = []

    for entry in entries:
        errors.extend(check_entry(entry, recipes))

    if not entries:
        errors.append(
            f"no recipes found under {base_dir}; refusing to report success"
        )

    return errors, len(entries)


def check_dependencies(base_dir: Path = RECIPES_DIR) -> list[str]:
    """Return a list of human-readable errors, empty when all deps resolve."""
    return _check_dependencies(base_dir)[0]


def main(base_dir: Path = RECIPES_DIR) -> int:
    try:
        errors, count = _check_dependencies(base_dir)
    except AliasCollision as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print(
            "  two recipes answer to the same name; rename one directory or "
            "canonical_name",
            file=sys.stderr,
        )
        return 1
    except TypeError as exc:
        # A malformed dependencies field. Reported rather than raised, because
        # `make site` skips the checkers and reaches the generators directly.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if errors:
        print("ERROR: dependency validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1

    noun = "recipe" if count == 1 else "recipes"
    print(f"All dependencies resolve ({count} {noun})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
