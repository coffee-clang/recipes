#!/usr/bin/env python3
import tomllib
import json
from pathlib import Path

OUTPUT = "docs/.well-known/packages.json"

packages = []

for toml_file in sorted(Path("recipes").rglob("library.toml")):
    dir_path = toml_file.parent

    with open(toml_file, "rb") as f:
        data = tomllib.load(f)

    canonical_name = data.get("canonical_name", "")
    if not canonical_name:
        canonical_name = dir_path.name

    packages.append(
        {
            "name": data.get("title", ""),
            "canonical_name": canonical_name,
            "description": data.get("description", ""),
            "version": data.get("version", ""),
        }
    )

with open(OUTPUT, "w") as f:
    json.dump(packages, f, indent=2)

print(f"Packages written to {OUTPUT}")
