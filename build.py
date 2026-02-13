#!/usr/bin/env python3
import sys
import tomllib

def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <input.toml> <output.html> <template.html>", file=sys.stderr)
        sys.exit(1)
    
    input_toml = sys.argv[1]
    output_html = sys.argv[2]
    template_html = sys.argv[3]
    
    # Read TOML
    with open(input_toml, "rb") as f:
        data = tomllib.load(f)
    
    title = data.get("title", "")
    version = data.get("version", "")
    description = data.get("description", "")
    license = data.get("license", "")
    dependencies = data.get("dependencies", "")
    
    # Generate markdown
    md_content = f"""# {title}

## Version
{version}

## License
{license}

## Dependencies
{dependencies}

## Recipe
[Install Script](./install.sh)
"""
    
    # Get last updated from git
    import subprocess
    import os
    dir_path = os.path.dirname(input_toml)
    try:
        result = subprocess.run(
            ["git", "-C", dir_path, "log", "-1", "--format=%cd", "--date=format:%Y-%m-%d"],
            capture_output=True, text=True
        )
        last_updated = result.stdout.strip() or ""
    except:
        last_updated = ""
    
    if last_updated:
        md_content += f"\n## Last Update\n{last_updated}\n"
    
    # Convert markdown to HTML using lowdown
    import subprocess
    proc = subprocess.Popen(["lowdown"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    html_content, _ = proc.communicate(input=md_content.encode())
    html_content = html_content.decode()
    
    # Read template
    with open(template_html, "r") as f:
        template = f.read()
    
    # Replace placeholders
    output = template.replace("{{ title }}", title)
    output = output.replace("{{ content }}", html_content)
    
    # Write output
    with open(output_html, "w") as f:
        f.write(output)

if __name__ == "__main__":
    main()
