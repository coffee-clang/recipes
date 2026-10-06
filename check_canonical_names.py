#!/usr/bin/env python3
"""Validate recipe canonical names.

A canonical name becomes a prefix for generated variables and functions, so it
must be a valid C identifier: letters, digits, and underscores only, never
leading with a digit. Dashes are rejected because they cannot appear in a C
identifier.
"""

import sys
from typing import NamedTuple

from recipe_metadata import RECIPES_DIR, load_recipe, recipe_files

# Canonical names are embedded in C identifiers, so the alphabet is restricted
# to what a C identifier can contain. Dashes are excluded on purpose.
FORBIDDEN_CHARS = set("-.")


def is_valid_canonical_name(name: str) -> bool:
    """Return True when name is usable as a C identifier prefix."""
    if not name:
        return False
    # Explicit isascii() checks: str.isalnum() accepts 'ï' and many other
    # unicode letters, which cannot appear in a C identifier.
    if not name[0].isascii():
        return False
    if not (name[0].isalpha() or name[0] == "_"):
        return False
    if any(c in FORBIDDEN_CHARS for c in name):
        return False
    return all(c.isascii() and (c.isalnum() or c == "_") for c in name)


def refusal_message(base_dir) -> str:
    """Return the empty-tree refusal message."""
    return f"no recipes found under {base_dir}; refusing to report success"


class NameCheckResult(NamedTuple):
    """Outcome of a canonical-name check.

    Field order (duplicates, invalid, tree_errors, count) is part of the
    contract: callers unpack it positionally as well as by name.
    """

    duplicates: list[str]
    invalid: list[str]
    tree_errors: list[str]
    count: int


def check_canonical_names(
    base_dir=RECIPES_DIR,
) -> NameCheckResult:
    """Return a NameCheckResult.

    tree_errors holds failures that are not about any one name: the empty-tree
    refusal and unreadable recipes. count is the number of recipes found, so
    callers do not re-walk the tree.
    """
    files = recipe_files(base_dir)
    if not files:
        return NameCheckResult([], [], [refusal_message(base_dir)], 0)

    canonical_names: dict[str, object] = {}
    duplicates: list[str] = []
    invalid: list[str] = []
    tree_errors: list[str] = []

    for toml_file in files:
        try:
            data = load_recipe(toml_file)
        except TypeError as exc:
            # A malformed library.toml must not traceback out of the checker;
            # report it and keep going so one bad file cannot hide the rest of
            # the tree's problems. It is a tree-level failure, not an invalid
            # name, so it goes in tree_errors and is never printed under the
            # names header.
            tree_errors.append(f"{toml_file}: unreadable recipe: {exc}")
            continue
        dir_path = toml_file.parent

        canonical_name = data.get("canonical_name", "")
        if not canonical_name:
            canonical_name = dir_path.name

        if not is_valid_canonical_name(canonical_name):
            bad = sorted(c for c in FORBIDDEN_CHARS if c in canonical_name)
            hint = ""
            if bad:
                hint = " (use " + ", ".join(
                    f"'{canonical_name.replace(c, '_')}' instead" for c in bad
                ) + ")"
            invalid.append(
                f"{toml_file}: canonical_name '{canonical_name}' is not a valid "
                f"C identifier{hint}"
            )

        if canonical_name in canonical_names:
            duplicates.append(
                f"'{canonical_name}' appears in:\n"
                f"    - {canonical_names[canonical_name]}\n"
                f"    - {dir_path}"
            )
        else:
            canonical_names[canonical_name] = dir_path

    return NameCheckResult(duplicates, invalid, tree_errors, len(files))


def main(base_dir=RECIPES_DIR) -> int:
    result = check_canonical_names(base_dir)
    errors = []

    if result.duplicates:
        errors.append("Duplicate canonical names found:")
        errors.extend(f"  {d}" for d in result.duplicates)

    if result.invalid:
        errors.append("Invalid canonical names found:")
        errors.extend(f"  {e}" for e in result.invalid)

    # Tree-level failures (the empty-tree refusal, unreadable recipes) are
    # printed under the general header, never under a name-level one.
    errors.extend(f"  {e}" for e in result.tree_errors)

    if errors:
        print("ERROR: canonical name validation failed:", file=sys.stderr)
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(
        f"No invalid or duplicate canonical names "
        f"({result.count} libraries checked)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
