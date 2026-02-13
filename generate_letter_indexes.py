#!/usr/bin/env python3
import tomllib
import subprocess
import os
from pathlib import Path


def get_last_updated(dir_path: Path) -> str:
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
        return result.stdout.strip() or ""
    except:
        return ""


def generate_letter_pages():
    libraries_by_letter: dict[str, list[dict]] = {}

    base_dir = Path("recipes")
    for letter_dir in sorted(base_dir.iterdir()):
        if not letter_dir.is_dir() or len(letter_dir.name) != 1:
            continue

        letter = letter_dir.name.upper()
        libraries_by_letter[letter] = []

        for lib_dir in sorted(letter_dir.iterdir()):
            if not lib_dir.is_dir():
                continue

            toml_path = lib_dir / "library.toml"
            if not toml_path.exists():
                continue

            with open(toml_path, "rb") as f:
                data = tomllib.load(f)

            libraries_by_letter[letter].append(
                {
                    "name": lib_dir.name,
                    "version": data.get("version", ""),
                    "license": data.get("license", ""),
                    "last_updated": get_last_updated(lib_dir),
                }
            )

    template_path = Path("templates/template.html")
    with open(template_path, "r") as f:
        template = f.read()

    for letter, libraries in libraries_by_letter.items():
        if not libraries:
            continue

        letter_dir = base_dir / letter.lower()
        letter_dir.mkdir(exist_ok=True)
        output_path = letter_dir / "index.html"

        rows = []
        for lib in libraries:
            lib_path = f"{lib['name']}/"
            rows.append(f"""<tr>
<td><a href="{lib_path}">{lib["name"]}</a></td>
<td>{lib["version"]}</td>
<td>{lib["license"]}</td>
<td>{lib["last_updated"]}</td>
</tr>""")

        html_content = f"""<h1>C Libraries - {letter}</h1>

<table>
<thead>
<tr>
<th>Package</th>
<th>Version</th>
<th>License</th>
<th>Last Updated</th>
</tr>
</thead>
<tbody>
{"".join(rows)}
</tbody>
</table>

<p>Total: {len(libraries)} packages starting with {letter}</p>
"""

        output = template.replace("{{ title }}", f"Cup of Coffee - {letter}")
        output = output.replace("{{ content }}", html_content)

        with open(output_path, "w") as f:
            f.write(output)

        print(f"Generated: {output_path}")


if __name__ == "__main__":
    generate_letter_pages()
