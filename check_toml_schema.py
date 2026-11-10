import re
import sys
import tomllib
from pathlib import PurePosixPath

from recipe_metadata import (
    BUILD_DEPENDENCIES_FIELD,
    RECIPES_DIR,
    dependencies_type_error,
    recipe_files,
)

MANDATORY_FIELDS = (
    "title",
    "version",
    "description",
    "license",
    "recipe_url",
    "canonical_name",
    "output_type",
    "dependencies",
    "sha256",
    "sha256_source",
)
DEPENDENCIES_FIELD = "dependencies"
# "data" installs files other builds read, such as protocol descriptions.
VALID_OUTPUT_TYPES = frozenset({"library", "executable", "both", "data"})

# Output types a consumer links against, so they must say how: a libname for
# -l<libname>, or header_only = true.
LINKABLE_OUTPUT_TYPES = frozenset({"library", "both"})

# The published script checks the download against sha256 before extracting.
# sha256_source says how far the digest is trusted: published by upstream,
# taken from a release whose signature was verified, or trust-on-first-use.
SHA256 = re.compile(r"[0-9a-f]{64}")
SHA256_SOURCES = ("upstream", "signature", "tofu")

# Optional subdirectories of the install prefix, defaulting to include and lib.
PREFIX_DIR_FIELDS = ("include_dir", "lib_dir")

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
            f"'both' or 'data', got '{data['output_type']}'"
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

    build_dependencies = data.get(BUILD_DEPENDENCIES_FIELD)
    if build_dependencies is not None and not isinstance(build_dependencies,
                                                         dict):
        message = dependencies_type_error(build_dependencies,
                                          BUILD_DEPENDENCIES_FIELD)
        errors.append(f"{name}: {message}")

    errors.extend(f"{name}: {e}" for e in usage_errors(data))
    errors.extend(f"{name}: {e}" for e in digest_errors(data))
    return errors


def digest_errors(data) -> list[str]:
    """Return errors in the download digest fields, when present."""
    errors = []
    digest = data.get("sha256")
    if digest is not None and not (isinstance(digest, str)
                                   and SHA256.fullmatch(digest)):
        errors.append("sha256 must be 64 lowercase hexadecimal digits")
    source = data.get("sha256_source")
    if source is not None and source not in SHA256_SOURCES:
        errors.append(f"sha256_source must be one of "
                      f"{', '.join(SHA256_SOURCES)}, got {source!r}")
    return errors


def is_libname(value) -> bool:
    """A libname is a non-empty string, or a non-empty list of them."""
    values = value if isinstance(value, list) else [value]
    return bool(values) and all(isinstance(v, str) and v.strip()
                                for v in values)


def usage_errors(data) -> list[str]:
    """Return errors in the fields that say how to use the installed library."""
    errors = []
    libname = data.get("libname")
    header_only = data.get("header_only", False)

    if libname is not None and not is_libname(libname):
        errors.append("libname must be a non-empty string or list of strings")
    if not isinstance(header_only, bool):
        errors.append("header_only must be true or false")
    elif header_only and libname is not None:
        errors.append("header_only = true contradicts libname: a header-only "
                      "library has nothing to link")
    elif (not header_only and libname is None
          and data.get("output_type") in LINKABLE_OUTPUT_TYPES):
        errors.append("a library must set libname or header_only = true")

    for field in PREFIX_DIR_FIELDS:
        value = data.get(field)
        if value is None:
            continue
        path = PurePosixPath(value) if isinstance(value, str) else None
        if (path is None or not value.strip() or path.is_absolute()
                or ".." in path.parts):
            errors.append(f"{field} must be a relative path inside the "
                          f"prefix, got {value!r}")

    if "notes" in data and not isinstance(data["notes"], str):
        errors.append("notes must be a string")
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
