#!/usr/bin/env python3
import tomllib
import subprocess
import os
from pathlib import Path

OUTPUT = "summary.csv"

# Write header
with open(OUTPUT, "w") as f:
    f.write("library_name,version,link,license,last_updated\n")

# Find all library.toml files
for toml_file in sorted(Path("recipes").rglob("library.toml")):
    dir_path = toml_file.parent
    library_name = dir_path.name

    with open(toml_file, "rb") as f:
        data = tomllib.load(f)

    version = data.get("version", "")
    link = data.get("recipe_url", "")
    license = data.get("license", "")

    # Get last updated from git
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(dir_path),
                "log",
                "-1",
                "--format=%cd",
                "--date=format:%Y-%m-%d",
            ],
            capture_output=True,
            text=True,
        )
        last_updated = result.stdout.strip() or ""
    except:
        last_updated = ""

    with open(OUTPUT, "a") as f:
        f.write(f'"{library_name}","{version}","{link}","{license}","{last_updated}"\n')

print(f"Summary written to {OUTPUT}")
