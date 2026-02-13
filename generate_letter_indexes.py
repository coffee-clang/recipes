#!/usr/bin/env python3
import tomllib
import subprocess
import math
from pathlib import Path


PAGE_SIZE = 50


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

        letter_lower = letter.lower()
        letter_dir = base_dir / letter_lower
        letter_dir.mkdir(exist_ok=True)

        total_pages = math.ceil(len(libraries) / PAGE_SIZE)

        for page_num in range(total_pages):
            start_idx = page_num * PAGE_SIZE
            end_idx = min(start_idx + PAGE_SIZE, len(libraries))
            page_libraries = libraries[start_idx:end_idx]

            if page_num == 0:
                output_path = letter_dir / "index.html"
            else:
                page_dir = letter_dir / str(page_num)
                page_dir.mkdir(exist_ok=True)
                output_path = page_dir / "index.html"

            rows = []
            for lib in page_libraries:
                lib_path = f"{lib['name']}/"
                rows.append(f"""<tr>
<td><a href="{lib_path}">{lib["name"]}</a></td>
<td>{lib["version"]}</td>
<td>{lib["license"]}</td>
<td>{lib["last_updated"]}</td>
</tr>""")

            pagination = ""
            if total_pages > 1:
                pagination = '<p class="pagination">'
                if page_num > 0:
                    prev_link = (
                        str(page_num - 1) + "/index.html"
                        if page_num > 1
                        else "index.html"
                    )
                    pagination += f'<a href="{prev_link}">&laquo; Previous</a> '
                pagination += f"Page {page_num + 1} of {total_pages}"
                if page_num < total_pages - 1:
                    next_link = f"{page_num + 1}/index.html"
                    pagination += f' <a href="{next_link}">Next &raquo;</a>'
                pagination += "</p>"

            if page_num == 0:
                page_title = f"Cup of Coffee - {letter}"
            else:
                page_title = f"Cup of Coffee - {letter} [Page {page_num + 1}]"

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

{pagination}

<p>Total: {len(libraries)} packages starting with {letter}</p>
"""

            output = template.replace("{{ title }}", page_title)
            output = output.replace("{{ content }}", html_content)

            with open(output_path, "w") as f:
                f.write(output)

            print(f"Generated: {output_path}")


if __name__ == "__main__":
    generate_letter_pages()
