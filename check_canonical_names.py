#!/usr/bin/env python3
import tomllib
import sys
from pathlib import Path

canonical_names = {}
duplicates = []

for toml_file in Path("recipes").rglob("library.toml"):
    dir_path = toml_file.parent

    with open(toml_file, "rb") as f:
        data = tomllib.load(f)

    canonical_name = data.get("canonical_name", "")
    if not canonical_name:
        canonical_name = dir_path.name

    if canonical_name in canonical_names:
        duplicates.append((canonical_name, canonical_names[canonical_name], dir_path))
    else:
        canonical_names[canonical_name] = dir_path

if duplicates:
    print("ERROR: Duplicate canonical names found:", file=sys.stderr)
    for canonical_name, orig_path, dup_path in duplicates:
        print(f"  '{canonical_name}' appears in:", file=sys.stderr)
        print(f"    - {orig_path}", file=sys.stderr)
        print(f"    - {dup_path}", file=sys.stderr)
    sys.exit(1)

print(f"No duplicate canonical names found ({len(canonical_names)} libraries checked)")
