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
