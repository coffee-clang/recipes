#!/usr/bin/env python3
"""Generate package JSON files for the recipe catalog.

For each recipe, generates:
  docs/<letter>/<dir-name>/<title>.json  — per-recipe JSON (all page fields)
  docs/.well-known/packages.json         — aggregate index

The <letter> and <dir-name> path components mirror where mdBook emits the
recipe's HTML page, so a client that resolves a page path finds its JSON. The
filename uses <title> because titles are human-facing; the directory component
already disambiguates, so title uniqueness is not required.
"""

import json
import sys
from pathlib import Path

from recipe_metadata import (
    RECIPES_DIR,
    REPO_ROOT,
    get_last_updated,
    load_recipe,
    recipe_build_dependencies,
    recipe_dependencies,
    recipe_files,
    recipe_letter,
    recipe_usage,
)

DOCS_DIR = REPO_ROOT / "docs"


def recipe_json_path(toml_file: Path, title: str,
                     docs_dir: Path = DOCS_DIR) -> Path:
    """Return where a recipe's JSON must land to sit beside its HTML page."""
    return (docs_dir / recipe_letter(toml_file) / toml_file.parent.name
            / f"{title}.json")


def version_data(toml_file: Path, data: dict) -> dict:
    """Return the per-version payload for one recipe."""
    return {
        "version": data.get("version", ""),
        "canonical_name": data.get("canonical_name") or toml_file.parent.name,
        "description": data.get("description", ""),
        "license": data.get("license", ""),
        "dependencies": recipe_dependencies(toml_file, data),
        "build_dependencies": recipe_build_dependencies(toml_file, data),
        "recipe_url": data.get("recipe_url", ""),
        "output_type": data.get("output_type", ""),
        "last_updated": get_last_updated(toml_file.parent),
        **recipe_usage(data),
    }


def main(recipes_dir: Path = RECIPES_DIR, docs_dir: Path = DOCS_DIR) -> int:
    """Write every recipe JSON plus the aggregate index. Returns an exit code."""
    packages = []

    try:
        records = []
        for toml_file in recipe_files(recipes_dir):
            data = load_recipe(toml_file)
            records.append(
                (toml_file, data.get("title", toml_file.parent.name),
                 version_data(toml_file, data))
            )
    except TypeError as exc:
        # `make site` skips the checkers, so a malformed field can reach here
        # directly. Report it the way the checkers do instead of raising.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    for toml_file, title, info in records:
        # The aggregate index entry carries the name for identification.
        packages.append({"name": title, **info})

        recipe_json = recipe_json_path(toml_file, title, docs_dir)
        recipe_json.parent.mkdir(parents=True, exist_ok=True)
        recipe_json.write_text(
            json.dumps({"name": title, "versions": [info]}, indent=2)
        )
        print(f"  Generated {recipe_json}")

    index = docs_dir / ".well-known" / "packages.json"
    index.parent.mkdir(parents=True, exist_ok=True)
    index.write_text(json.dumps(packages, indent=2))
    print(f"Packages written to {index} ({len(packages)} packages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
