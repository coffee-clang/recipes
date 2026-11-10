#!/usr/bin/env python3
"""Read the pure part of an install.sh, for the suites that execute it.

Two test modules expand a recipe's leading assignments in a real bash process
so an unbound variable shows up at runtime instead of only at review time.
Both need the same thing: the lines that assign variables, and nothing else.

"Nothing else" is the whole point. The extracted lines get *executed*, so
stopping one line too late runs a side effect — a `WORK="$(mktemp -d)"` that
creates and leaks a directory. Hence two stop markers: `ARCHIVE=`, which
derives a name from the URL, and `WORK=`, the first line whose effect reaches
the filesystem.
"""

import re
import shlex

# An assignment, allowing for an `export` in front. Only lines that match are
# collected, so a command carrying an argument with "=" in it never lands here.
ASSIGNMENT = re.compile(r"^\s*(?:export\s+)?[A-Za-z_]\w*=")

# Execution stops at the first of these. WORK= matters even when ARCHIVE= is
# absent, which is the case for every git-clone recipe.
STOP_LINES = ("ARCHIVE=", "WORK=")


def is_stop_line(line: str) -> bool:
    """Return True for a line that must not be executed."""
    return re.sub(r"^\s*(?:export\s+)?", "", line).startswith(STOP_LINES)


def header_assignments(script) -> list[str]:
    """Return the leading assignment lines of a recipe's install.sh.

    Skips the shebang and any `set ` line. Returns an empty list for a script
    that declares no variables; callers must treat that as a defect rather
    than as "nothing to expand", since expanding nothing silently disables
    every check that depends on the header.
    """
    header = []
    for line in script.read_text().splitlines():
        if line.startswith(("#!", "set ")):
            continue
        if is_stop_line(line):
            break
        if ASSIGNMENT.match(line):
            header.append(line)
    return header


# The first two lines of every install.sh template in the repository.
TEMPLATE_PREAMBLE = "#!/bin/bash\nset -e -o pipefail -u\n"

# Generated in front of the template body. library.toml is the only place
# that names the package, version and URL, so the template reads these and
# never assigns them. The prefix is the first argument when given, made
# absolute because the body runs inside the scratch directory.
HEADER = """\
# Generated from library.toml by generate_mdbook_src.py.
PACKAGE={package}
VERSION={version}
URL={url}
SHA256={sha256}
COFFEE_HOME="${{COFFEE_HOME:-$HOME/.coffee}}"
PREFIX="${{1:-$COFFEE_HOME/$PACKAGE/$VERSION}}"
case "$PREFIX" in /*) ;; *) PREFIX="$PWD/$PREFIX" ;; esac
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
ARCHIVE="$(basename "$URL")"
wget -q "$URL"
# Nothing from the archive is read until its digest matches library.toml.
printf '%s  %s\\n' "$SHA256" "$ARCHIVE" | sha256sum -c --quiet -
"""

HEADER_VARIABLES = ("PACKAGE", "VERSION", "URL", "SHA256", "COFFEE_HOME",
                    "PREFIX", "WORK", "ARCHIVE")

# Any fetch in a template would bypass the digest the header checks.
DOWNLOAD = re.compile(r"^\s*(?:wget|curl)\b|\bgit\s+clone\b")


def template_errors(template: str) -> list[str]:
    """Return why a template cannot be rendered, empty when it can."""
    errors = []
    if not template.startswith(TEMPLATE_PREAMBLE):
        errors.append("template must start with "
                      f"{TEMPLATE_PREAMBLE.strip()!r}")
    for line in template.splitlines():
        match = ASSIGNMENT.match(line)
        name = match and re.sub(r"^\s*(?:export\s+)?", "", line).split("=")[0]
        if name in HEADER_VARIABLES:
            errors.append(f"template assigns {name}, which the generated "
                          f"header owns: {line.strip()!r}")
        if DOWNLOAD.search(line) and not line.lstrip().startswith("#"):
            errors.append(f"template downloads outside the verified header "
                          f"fetch: {line.strip()!r}")
    return errors


def render_install_script(template: str, data: dict) -> str:
    """Return the published install.sh: preamble, header, template body."""
    errors = template_errors(template)
    if errors:
        raise ValueError("; ".join(errors))
    header = HEADER.format(
        package=shlex.quote(data["canonical_name"]),
        version=shlex.quote(data["version"]),
        url=shlex.quote(data["recipe_url"]),
        sha256=shlex.quote(data["sha256"]),
    )
    body = template[len(TEMPLATE_PREAMBLE):]
    return f"{TEMPLATE_PREAMBLE}\n{header}{body}"
