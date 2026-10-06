#!/usr/bin/env python3
"""Shared recipe metadata helpers.

Single source of truth for locating the recipe tree and for reading a recipe's
metadata. Both site generators and all three checkers go through here, so a
recipe is discovered and parsed the same way everywhere.
"""

import subprocess
import tomllib
import warnings
from functools import lru_cache
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
RECIPES_DIR = REPO_ROOT / "recipes"

# Seconds to wait for a single `git log`. A slow or wedged repository must not
# hang the build.
GIT_TIMEOUT = 5


def recipe_files(base_dir: Path = RECIPES_DIR) -> list[Path]:
    """Return every library.toml under base_dir, in a stable order."""
    return sorted(Path(base_dir).rglob("library.toml"))


def recipe_letter(toml_file: Path) -> str:
    """Return the lowercase letter bucket for a recipe, from its directory.

    Derived from the path, never from the title: a recipe may be titled
    ``libexif`` while living in ``recipes/e/exif/``, and the site routes on the
    directory.
    """
    return toml_file.parent.parent.name.lower()


def load_recipe(toml_file: Path) -> dict:
    """Parse one library.toml.

    A syntax error or an unreadable file (invalid UTF-8, a directory, a
    permission problem) is reported as a TypeError naming the recipe, the
    same shape recipe_dependencies uses for a malformed field, so every
    consumer's existing handler reports it the same way.
    """
    try:
        with open(toml_file, "rb") as f:
            return tomllib.load(f)
    except (tomllib.TOMLDecodeError, UnicodeDecodeError, OSError) as exc:
        raise TypeError(f"{toml_file.parent.name}: {exc}") from None


def recipe_names(toml_file: Path, data: dict) -> set[str]:
    """Return the names this recipe answers to: canonical_name and directory.

    The directory name is an alias in its own right. Eight recipes keep their
    upstream dashed spelling in the directory (``recipes/j/json-c/``) while
    their C-identifier canonical name is underscored, and dependents refer to
    them by the spelling their upstream uses.
    """
    return {
        data.get("canonical_name") or toml_file.parent.name,
        toml_file.parent.name,
    }


# One wording for the type error, shared by every module that raises it. The
# schema checker and this parser used to phrase the same failure differently,
# which sent the reader from one file to the other to learn the same thing.
_DEPENDENCIES_TYPE_ERROR = ("dependencies must be a [dependencies] table, "
                            "not a {}")


def dependencies_type_error(raw) -> str:
    """Return the canonical message for a non-table dependencies field."""
    return _DEPENDENCIES_TYPE_ERROR.format(type(raw).__name__)


def parse_dependencies(raw) -> dict[str, str]:
    """Normalize the dependency table to {name: constraint}.

    The schema requires a ``[dependencies]`` table, possibly empty, so a
    missing field and an empty table both mean "no dependencies". A constraint
    is retained verbatim; an empty string means "any version".

    A string is rejected rather than parsed. The old parser split strings on
    whitespace, which read ``dependencies = "None"`` as three packages named
    None, of and these, and reported a dependency-resolution failure for a
    recipe that declared nothing.
    """
    if raw is None:
        return {}
    if isinstance(raw, dict):
        return {str(k): str(v) for k, v in raw.items()}
    raise TypeError(dependencies_type_error(raw))


def recipe_dependencies(toml_file: Path, data: dict) -> dict[str, str]:
    """Return one recipe's dependencies, naming the recipe when malformed.

    Every consumer goes through here instead of calling parse_dependencies
    directly, so a field error always says which recipe is at fault rather than
    leaving the reader to search the tree for it.
    """
    try:
        return parse_dependencies(data.get("dependencies"))
    except TypeError as exc:
        raise TypeError(f"{toml_file.parent.name}: {exc}") from None


@lru_cache(maxsize=None)
def get_last_updated(dir_path: Path) -> str:
    """Return the ISO date of the last commit touching a recipe directory.

    Both site generators render this, and a build makes 114 calls each, so the
    result is cached: one git subprocess per recipe instead of two.

    Returns an empty string when git is unavailable or too slow, but warns
    rather than failing silently — a blank "Last Updated" column on every page
    looks like data, not like a broken environment.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(dir_path), "log", "-1", "--format=%cd",
             "--date=format:%Y-%m-%d"],
            capture_output=True, text=True, timeout=GIT_TIMEOUT, check=True,
        )
    except (subprocess.SubprocessError, OSError) as exc:
        warnings.warn(
            f"cannot read last-updated date for {dir_path}: {exc}",
            UserWarning,
            stacklevel=2,
        )
        return ""
    return result.stdout.strip()
