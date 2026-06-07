#!/usr/bin/env python3
"""Generate package JSON files for the recipe catalog.

For each recipe, generates:
  docs/<letter>/<name>/<name>.json  — per-recipe JSON (all page fields)
  docs/.well-known/packages.json    — aggregate index
"""

import subprocess
import tomllib
import json
from pathlib import Path

BASE_DIR = Path("recipes")
OUTPUT = "docs/.well-known/packages.json"


def parse_dependencies(dep: str | dict | None) -> dict[str, str]:
    """Normalize dependencies to a dict: {pkg_name: version_constraint}.

    Accepts a TOML table (dict), a string, or None.
    Empty string means 'any version is fine'.
    """
    if dep is None:
        return {}
    if isinstance(dep, dict):
        return {str(k): str(v) for k, v in dep.items()}
    s = dep.strip()
    if not s or s.lower().startswith("none"):
        return {}
    parts = [p.strip() for p in s.replace(",", " ").split() if p.strip()]
    result = {}
    for part in parts:
        # Strip parenthetical annotations like "(optional)", "(build)"
        name = part.split("(")[0].strip().rstrip(")")
        if name:
            result[name] = ""
    return result


def get_last_updated(dir_path: Path) -> str:
    """Get the last commit date for a recipe directory."""
    try:
        result = subprocess.run(
            ["git", "-C", str(dir_path), "log", "-1", "--format=%cd",
             "--date=format:%Y-%m-%d"],
            capture_output=True, text=True, timeout=5,
        )
        return result.stdout.strip() or ""
    except Exception:
        return ""


packages = []

for toml_file in sorted(BASE_DIR.rglob("library.toml")):
    dir_path = toml_file.parent
    lib_name = dir_path.name

    with open(toml_file, "rb") as f:
        data = tomllib.load(f)

    name = data.get("title", lib_name)
    canonical_name = data.get("canonical_name", "")
    if not canonical_name:
        canonical_name = lib_name

    # Build two representations:
    #   - version_data: fields that may differ per version (no name — it's per-package)
    #   - flat_entry:   aggregate index entry (includes name for identification)
    deps = parse_dependencies(data.get("dependencies"))

    version_data = {
        "version": data.get("version", ""),
        "canonical_name": canonical_name,
        "description": data.get("description", ""),
        "license": data.get("license", ""),
        "dependencies": deps,
        "recipe_url": data.get("recipe_url", ""),
        "last_updated": get_last_updated(dir_path),
    }
    flat_entry = {"name": name, **version_data}
    packages.append(flat_entry)

    # Write per-recipe JSON alongside the mdBook-generated HTML page
    letter = name[0].lower()
    recipe_dir = Path("docs") / letter / lib_name
    recipe_dir.mkdir(parents=True, exist_ok=True)
    recipe_json = recipe_dir / f"{name}.json"

    # Schema: top-level name + array of versions (supports future multi-version)
    recipe_entry = {
        "name": name,
        "versions": [version_data],
    }
    with open(recipe_json, "w") as f:
        json.dump(recipe_entry, f, indent=2)
    print(f"  Generated {recipe_json}")

# Write aggregate index
Path("docs/.well-known").mkdir(parents=True, exist_ok=True)
with open(OUTPUT, "w") as f:
    json.dump(packages, f, indent=2)

print(f"Packages written to {OUTPUT}")
