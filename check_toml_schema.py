import sys
import tomllib

from recipe_metadata import RECIPES_DIR, dependencies_type_error, recipe_files

MANDATORY_FIELDS = (
    "title",
    "version",
    "description",
    "license",
    "recipe_url",
    "canonical_name",
    "output_type",
    "dependencies",
)
DEPENDENCIES_FIELD = "dependencies"
VALID_OUTPUT_TYPES = frozenset({"library", "executable", "both"})

# The title becomes a filename in generate_packages.py, so it may not contain a
# path separator or a component that is not a plain file name.
TITLE_FORBIDDEN = ("/", "\\", "..")


def check_recipe(toml_file, data) -> list[str]:
    """Return the schema errors for one parsed recipe."""
    errors = []
    name = toml_file.parent.name

    # Presence and blankness are different failures: an empty [dependencies]
    # table is a recipe that declares nothing, which is valid, whereas
    # license = "" is a field the author forgot to fill in.
    missing = [
        f for f in MANDATORY_FIELDS
        if f not in data or (isinstance(data[f], str) and not data[f].strip())
    ]
    if missing:
        errors.append(f"{name}: missing fields: {', '.join(missing)}")

    if "output_type" in data and data["output_type"] not in VALID_OUTPUT_TYPES:
        errors.append(
            f"{name}: output_type must be 'library', 'executable', "
            f"or 'both', got '{data['output_type']}'"
        )

    title = data.get("title")
    if isinstance(title, str) and any(bad in title for bad in TITLE_FORBIDDEN):
        errors.append(
            f"{name}: title '{title}' must not contain "
            f"{', '.join(repr(b) for b in TITLE_FORBIDDEN)}; it is used as a "
            f"filename"
        )

    dependencies = data.get(DEPENDENCIES_FIELD)
    if dependencies is not None and not isinstance(dependencies, dict):
        # A table is the only accepted form. Strings were previously split on
        # whitespace, which read "None" as three packages named None, of these.
        errors.append(f"{name}: {dependencies_type_error(dependencies)}")

    return errors


def _check_recipes(base_dir) -> tuple[list[str], int]:
    """Return (errors, count) from a single tree walk."""
    files = recipe_files(base_dir)
    if not files:
        return [
            f"no recipes found under {base_dir}; refusing to report success"
        ], 0

    errors = []
    for toml_file in files:
        try:
            # Parsed here rather than through recipe_metadata.load_recipe: this
            # is the one place that must survive a malformed file, so it needs
            # to catch decode errors per recipe, name the file that failed, and
            # keep going so one bad file cannot hide the rest of the tree's
            # problems.
            with open(toml_file, "rb") as f:
                data = tomllib.load(f)
        except (tomllib.TOMLDecodeError, UnicodeDecodeError, OSError) as exc:
            errors.append(f"{toml_file.parent.name}: unreadable recipe: {exc}")
            continue
        errors.extend(check_recipe(toml_file, data))

    return errors, len(files)


def check_toml_schemas(base_dir=RECIPES_DIR) -> list[str]:
    """Return human-readable errors, empty when every recipe is valid."""
    return _check_recipes(base_dir)[0]


def main(base_dir=RECIPES_DIR) -> int:
    errors, count = _check_recipes(base_dir)
    if errors:
        print("ERROR: TOML validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1

    noun = "file is" if count == 1 else "files are"
    print(f"All {count} TOML {noun} valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
