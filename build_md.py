#!/usr/bin/env python3
import sys
import subprocess


def main():
    if len(sys.argv) < 4:
        print(
            f"Usage: {sys.argv[0]} <input.md> <output.html> <template.html>",
            file=sys.stderr,
        )
        sys.exit(1)

    input_md = sys.argv[1]
    output_html = sys.argv[2]
    template_html = sys.argv[3]

    # Extract title from YAML front matter
    title = ""
    with open(input_md, "r") as f:
        for line in f:
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip()
                break

    # Convert markdown to HTML using lowdown
    proc = subprocess.Popen(
        ["lowdown", "-s", input_md],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    html_content, _ = proc.communicate()
    html_content = html_content.decode()

    # Extract body content between <body> tags
    body_start = html_content.find("<body>") + 6
    body_end = html_content.find("</body>")
    body_content = html_content[body_start:body_end].strip()

    # Read template
    with open(template_html, "r") as f:
        template = f.read()

    # Replace placeholders
    output = template.replace("$title$", title)
    output = output.replace("$body$", body_content)

    # Write output
    with open(output_html, "w") as f:
        f.write(output)


if __name__ == "__main__":
    main()
