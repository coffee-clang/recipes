#!/usr/bin/env python3
import tomllib
import json
from pathlib import Path

OUTPUT = "docs/.well-known/packages.json"

packages = []

for toml_file in sorted(Path("recipes").rglob("library.toml")):
    with open(toml_file, "rb") as f:
        data = tomllib.load(f)

    packages.append(
        {
            "name": data.get("title", ""),
            "description": data.get("description", ""),
            "version": data.get("version", ""),
        }
    )

with open(OUTPUT, "w") as f:
    json.dump(packages, f, indent=2)

print(f"Packages written to {OUTPUT}")
