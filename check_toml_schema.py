#!/usr/bin/env python3
import tomllib
import sys
from pathlib import Path

MANDATORY_FIELDS = [
    "title",
    "version",
    "description",
    "license",
    "dependencies",
    "recipe_url",
    "canonical_name",
]

errors = []

for toml_file in sorted(Path("recipes").rglob("library.toml")):
    with open(toml_file, "rb") as f:
        data = tomllib.load(f)

    missing = [
        field for field in MANDATORY_FIELDS if field not in data or not data[field]
    ]

    if missing:
        errors.append(f"{toml_file}: missing fields: {', '.join(missing)}")

if errors:
    print("ERROR: TOML validation failed:", file=sys.stderr)
    for error in errors:
        print(f"  {error}", file=sys.stderr)
    sys.exit(1)

print(f"All {len(list(Path('recipes').rglob('library.toml')))} TOML files are valid")
