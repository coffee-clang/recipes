#!/usr/bin/env python3
"""Generate mdBook source files from recipe TOML files.

Reads recipes/<letter>/<name>/library.toml + install.sh and generates:
  src/<letter>/<name>/index.md     - Individual recipe page
  src/<letter>/<name>/install.sh   - Copied install script
  src/<letter>/index.md            - Letter index page
  src/index.md                     - Home page
  src/about.md                     - About page
  src/SUMMARY.md                   - Book table of contents
"""

import shutil
import subprocess
import tomllib
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("recipes")
SRC_DIR = Path("src")
PAGE_SIZE = 50  # Recipes per letter-index page (pagination for large letters)


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


def load_recipes() -> dict[str, list[dict]]:
    """Load all recipes, grouped by letter."""
    by_letter: dict[str, list[dict]] = {}

    for toml_file in sorted(BASE_DIR.rglob("library.toml")):
        letter = toml_file.parent.parent.name.upper()
        lib_name = toml_file.parent.name

        with open(toml_file, "rb") as f:
            data = tomllib.load(f)

        deps = parse_dependencies(data.get("dependencies"))

        by_letter.setdefault(letter, []).append({
            "name": lib_name,
            "title": data.get("title", lib_name),
            "canonical_name": data.get("canonical_name", lib_name),
            "version": data.get("version", ""),
            "description": data.get("description", ""),
            "license": data.get("license", ""),
            "dependencies": deps,
            "recipe_url": data.get("recipe_url", ""),
            "last_updated": get_last_updated(toml_file.parent),
        })

    return by_letter


def generate_recipe_page(lib: dict, letter_lower: str) -> str:
    """Generate the markdown content for a single recipe page."""
    lines = [
        f"# {lib['title']}",
        "",
        f"**Canonical name:** `{lib['canonical_name']}`",
        "",
        "## Version",
        "",
        lib["version"],
        "",
        "## License",
        "",
        lib["license"],
        "",
        "## Dependencies",
        "",
    ]

    deps = lib["dependencies"]
    if deps:
        for pkg, constraint in sorted(deps.items()):
            constraint_str = f" ({constraint})" if constraint else ""
            lines.append(f"- `{pkg}`{constraint_str}")
    else:
        lines.append("None")
    lines.append("")
    lines.append("## Recipe URL")
    lines.append("")
    lines.append(lib["recipe_url"] or "N/A")
    lines.append("")
    lines.append("## Install Script")
    lines.append("")
    lines.append(f"[Download install.sh](install.sh)")
    lines.append("")

    if lib["last_updated"]:
        lines.append("## Last Update")
        lines.append("")
        lines.append(lib["last_updated"])
        lines.append("")

    return "\n".join(lines)


def generate_letter_page(letter: str, libraries: list[dict],
                         letter_lower: str) -> str:
    """Generate the markdown content for a letter index page."""
    lines = [
        f"# C Libraries — {letter}",
        "",
        "| Package | Version | License | Last Updated |",
        "|---------|---------|---------|--------------|",
    ]

    for lib in libraries:
        # Link to the recipe page's index.html (mdbook makes index.md -> index.html)
        path = f"{lib['name']}/"
        lines.append(
            f"| [{lib['name']}]({path}) "
            f"| {lib['version']} "
            f"| {lib['license']} "
            f"| {lib['last_updated']} |"
        )

    lines.append("")
    lines.append(f"**Total: {len(libraries)} packages starting with {letter}**")
    lines.append("")

    return "\n".join(lines)


def generate_summary(by_letter: dict[str, list[dict]]) -> str:
    """Generate the SUMMARY.md content."""
    lines = ["# Summary", "", "[Home](index.md)", "[About](about.md)", "",
             "# Packages by Letter"]

    for letter in sorted(by_letter.keys()):
        letter_lower = letter.lower()
        libraries = sorted(by_letter[letter], key=lambda x: x["name"])
        lines.append("")
        lines.append(f"- [{letter}]({letter_lower}/index.md)")
        for lib in libraries:
            path = f"{letter_lower}/{lib['name']}/index.md"
            lines.append(f"    - [{lib['name']}]({path})")

    lines.append("")
    return "\n".join(lines)


def main():
    # Clean src directory (but keep theme/ if it exists)
    if SRC_DIR.exists():
        for item in SRC_DIR.iterdir():
            if item.name != "theme":
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
    SRC_DIR.mkdir(parents=True, exist_ok=True)

    by_letter = load_recipes()

    # Copy index.md and about.md into src/
    for page in ["index.md", "about.md"]:
        if Path(page).exists():
            shutil.copy2(page, SRC_DIR / page)
            print(f"  Copied {page} -> src/{page}")

    # No static assets to copy — CSS, logo loaded remotely from coffee-clang.github.io

    # Generate per-recipe and per-letter pages
    for letter in sorted(by_letter.keys()):
        letter_lower = letter.lower()
        libraries = sorted(by_letter[letter], key=lambda x: x["name"])

        # Create letter directory
        letter_dir = SRC_DIR / letter_lower
        letter_dir.mkdir(parents=True, exist_ok=True)

        # Generate letter index page
        letter_content = generate_letter_page(letter, libraries, letter_lower)
        (letter_dir / "index.md").write_text(letter_content)
        print(f"  Generated {letter_dir / 'index.md'} ({len(libraries)} recipes)")

        # Generate per-recipe pages
        for lib in libraries:
            lib_name = lib["name"]
            lib_dir = letter_dir / lib_name
            lib_dir.mkdir(parents=True, exist_ok=True)

            # Recipe markdown page
            recipe_content = generate_recipe_page(lib, letter_lower)
            (lib_dir / "index.md").write_text(recipe_content)

            # Copy install.sh
            src_install = BASE_DIR / letter_lower / lib_name / "install.sh"
            dst_install = lib_dir / "install.sh"
            if src_install.exists():
                shutil.copy2(src_install, dst_install)

            print(f"  Generated {lib_dir / 'index.md'}")

    # Generate SUMMARY.md
    summary = generate_summary(by_letter)
    (SRC_DIR / "SUMMARY.md").write_text(summary)
    print(f"  Generated SUMMARY.md ({len(summary)} chars)")

    total_recipes = sum(len(v) for v in by_letter.values())
    print(f"\nDone. {total_recipes} recipes across {len(by_letter)} letters.")


if __name__ == "__main__":
    main()