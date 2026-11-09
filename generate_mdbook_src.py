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
from recipe_script import render_install_script

SRC_DIR = REPO_ROOT / "src"

# Copied verbatim into src/ as the book's front matter.
FRONT_MATTER = ("index.md", "about.md")


def escape_cell(value: str) -> str:
    """Escape a value for use inside a Markdown table cell.

    Recipe metadata is free text, so a license or version containing a pipe
    would split one table row into two and shift every column after it; a
    newline would likewise break the row.

    Only the three metadata columns of the letter table are escaped. The
    Last Updated column is left alone: it is either an ISO date from git or an
    empty string, never free text.
    """
    return (str(value).replace("|", "\\|")
            .replace("\n", " ").replace("\r", " "))


def published_script(toml_file: Path, data: dict) -> str | None:
    """Return the install.sh users download, or None if the recipe has none.

    Rendered while loading, so a bad template stops the build before src/ is
    emptied, and the error names the recipe.
    """
    template = toml_file.parent / "install.sh"
    if not template.exists():
        return None
    try:
        return render_install_script(template.read_text(), data)
    except ValueError as exc:
        raise ValueError(f"{toml_file.parent.name}: {exc}") from None


def load_recipes(recipes_dir: Path = RECIPES_DIR) -> dict[str, list[dict]]:
    """Load all recipes, grouped by uppercase letter.

    Each record carries its own toml_file so callers never re-derive a path from
    the letter bucket and directory name.
    """
    by_letter: dict[str, list[dict]] = {}

    for toml_file in recipe_files(recipes_dir):
        data = load_recipe(toml_file)
        lib_name = toml_file.parent.name

        by_letter.setdefault(recipe_letter(toml_file).upper(), []).append({
            "toml_file": toml_file,
            "name": lib_name,
            "title": data.get("title", lib_name),
            "canonical_name": data.get("canonical_name", lib_name),
            "version": data.get("version", ""),
            "description": data.get("description", ""),
            "license": data.get("license", ""),
            "dependencies": recipe_dependencies(toml_file, data),
            "build_dependencies": recipe_build_dependencies(toml_file, data),
            "usage": recipe_usage(data),
            "install_script": published_script(toml_file, data),
            "recipe_url": data.get("recipe_url", ""),
            "output_type": data.get("output_type", ""),
            "last_updated": get_last_updated(toml_file.parent),
        })

    return by_letter


def dependency_list(deps: dict[str, str]) -> list[str]:
    """Return a sorted Markdown list of dependencies, or "None"."""
    if not deps:
        return ["None"]
    return [f"- `{pkg}`" + (f" ({constraint})" if constraint else "")
            for pkg, constraint in sorted(deps.items())]


def usage_lines(usage: dict) -> list[str]:
    """Return the Markdown that tells a consumer how to use the library."""
    if usage["header_only"]:
        lines = ["- Header-only: nothing to link"]
    else:
        flags = " ".join(f"-l{name}" for name in usage["libname"])
        lines = [f"- Link flags: `{flags}`"] if flags else []
        lines.append(f"- Library directory: `{usage['lib_dir']}`")
    lines.append(f"- Include directory: `{usage['include_dir']}`")
    if usage["notes"]:
        lines += ["", usage["notes"]]
    return lines


def generate_recipe_page(lib: dict) -> str:
    """Generate the markdown content for a single recipe page."""
    lines = [
        f"# {lib['title']}",
        "",
        f"**Canonical name:** `{lib['canonical_name']}`",
        "",
        f"**Output type:** {lib['output_type']}",
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

    lines += dependency_list(lib["dependencies"])
    lines += ["", "## Build Dependencies", ""]
    lines += dependency_list(lib["build_dependencies"])
    lines += ["", "## Usage", ""]
    lines += usage_lines(lib["usage"])
    lines += [
        "",
        "## Recipe URL",
        "",
        lib["recipe_url"] or "N/A",
        "",
        "## Install Script",
        "",
        "[Download install.sh](install.sh)",
        "",
    ]

    if lib["last_updated"]:
        lines += ["## Last Update", "", lib["last_updated"], ""]

    return "\n".join(lines)


def generate_letter_page(letter: str, libraries: list[dict]) -> str:
    """Generate the markdown content for a letter index page."""
    lines = [
        f"# C Libraries — {letter}",
        "",
        "| Package | Version | License | Last Updated |",
        "|---------|---------|---------|--------------|",
    ]

    for lib in libraries:
        lines.append(
            f"| [{escape_cell(lib['name'])}]({lib['name']}/) "
            f"| {escape_cell(lib['version'])} "
            f"| {escape_cell(lib['license'])} "
            f"| {lib['last_updated']} |"
        )

    lines += [
        "",
        f"**Total: {len(libraries)} packages starting with {letter}**",
        "",
    ]

    return "\n".join(lines)


def generate_summary(by_letter: dict[str, list[dict]]) -> str:
    """Generate the SUMMARY.md content."""
    lines = ["# Summary", "", "[Home](index.md)", "[About](about.md)", "",
             "# Packages by Letter"]

    for letter in sorted(by_letter):
        letter_lower = letter.lower()
        libraries = sorted(by_letter[letter], key=lambda x: x["name"])
        lines += ["", f"- [{letter}]({letter_lower}/index.md)"]
        for lib in libraries:
            lines.append(
                f"    - [{lib['name']}]"
                f"({letter_lower}/{lib['name']}/index.md)"
            )

    lines.append("")
    return "\n".join(lines)


def clean_src_dir(src_dir: Path) -> None:
    """Empty src/, keeping a theme directory if one is vendored there."""
    if src_dir.exists():
        for item in src_dir.iterdir():
            if item.name == "theme":
                continue
            shutil.rmtree(item) if item.is_dir() else item.unlink()
    src_dir.mkdir(parents=True, exist_ok=True)


def main(recipes_dir: Path = RECIPES_DIR, src_dir: Path = SRC_DIR) -> int:
    try:
        by_letter = load_recipes(recipes_dir)
    except (TypeError, ValueError) as exc:
        # `make site` skips the checkers, so a malformed field or template can
        # reach here directly. Report it the way the checkers do.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    clean_src_dir(src_dir)

    for page in FRONT_MATTER:
        source = REPO_ROOT / page
        if source.exists():
            shutil.copy2(source, src_dir / page)
            print(f"  Copied {page} -> src/{page}")

    # No static assets to copy — CSS and logo load remotely from
    # coffee-clang.github.io, so the site has no local asset pipeline.

    for letter in sorted(by_letter):
        letter_lower = letter.lower()
        libraries = sorted(by_letter[letter], key=lambda x: x["name"])

        letter_dir = src_dir / letter_lower
        letter_dir.mkdir(parents=True, exist_ok=True)

        letter_page = letter_dir / "index.md"
        letter_page.write_text(generate_letter_page(letter, libraries))
        print(f"  Generated {letter_page} ({len(libraries)} recipes)")

        for lib in libraries:
            lib_dir = letter_dir / lib["name"]
            lib_dir.mkdir(parents=True, exist_ok=True)

            page = lib_dir / "index.md"
            page.write_text(generate_recipe_page(lib))
            print(f"  Generated {page}")

            if lib["install_script"] is not None:
                published = lib_dir / "install.sh"
                published.write_text(lib["install_script"])
                published.chmod(0o755)

    summary = src_dir / "SUMMARY.md"
    text = generate_summary(by_letter)
    summary.write_text(text)
    print(f"  Generated SUMMARY.md ({len(text)} chars)")

    total = sum(len(v) for v in by_letter.values())
    print(f"\nDone. {total} recipes across {len(by_letter)} letters.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
