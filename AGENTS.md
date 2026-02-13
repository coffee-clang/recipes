# AGENTS.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

# Project-Specific Guidelines

## Project Overview

This repository contains recipes for building C libraries. Each recipe has:
- `library.toml` - metadata (title, version, license, dependencies, recipe_url)
- `install.sh` - installation script

The build system generates HTML documentation from these recipes using Python scripts.

## Build Commands

### Full Build
```bash
make                    # Build all HTML files from recipes
```

### Individual Steps
```bash
python3 ./generate_summary.py   # Generate summary.csv from all library.toml files
./generate_index.sh             # Generate index.html from summary.csv
```

### GitHub Actions (CI)
The CI workflow in `.github/workflows/build.yml` runs on push to main:
1. Installs `lowdown` (markdown to HTML converter)
2. Generates summary.csv
3. Generates index.html
4. Runs `make` to build all HTML files
5. Copies outputs to `docs/` folder
6. Deploys to GitHub Pages

**Important:** Never generate HTML files locally. Only generate them within the GitHub Actions workflow. Keep generated HTML files (.html) out of git commits.

### Linting
```bash
ruff check .            # Run ruff linter (if needed)
```

## Code Style Guidelines

### Python Scripts

**Imports:**
- Use standard library only: `tomllib`, `subprocess`, `os`, `pathlib`, `sys`
- Group imports: stdlib first, then third-party (none currently used)
- Use explicit imports (no `from x import *`)

**Formatting:**
- 4-space indentation
- Maximum line length: 88 characters (ruff default)
- Use f-strings for string formatting
- Use semantically meaningful variable names

**Functions:**
- Keep functions focused and small
- Use type hints when beneficial (Python 3.9+ available)
- Add docstrings for complex functions

**Error Handling:**
- Use `try/except` blocks with specific exception types when needed
- Prefer `sys.exit(1)` for fatal errors in CLI scripts
- Use `subprocess.run()` with `capture_output=True` instead of `check=True` for git commands to handle gracefully

**Example pattern:**
```python
#!/usr/bin/env python3
import sys
import tomllib
import subprocess
import os
from pathlib import Path
```

### Shell Scripts

**Shebang:** `#!/bin/bash` or `#!/usr/bin/env bash`

**Error Handling:**
- Always use `set -e` at the top to exit on errors
- Use `set -x` for debugging when needed

**Variables:**
- Use UPPERCASE for constants, lowercase for variables
- Always quote variables: `"$VAR"` not `$VAR`
- Use `${VAR}` for clarity in strings

**Example pattern (from install.sh):**
```bash
#!/bin/bash
set -e

SCRATCH="${1:-default_value}"
mkdir -p "$SCRATCH"

URL="https://example.com/archive.tar.gz"
cd /tmp
wget -q "$URL"
```

### TOML Recipe Files

Follow this schema for `library.toml`:
```toml
title = "PackageName"
version = "1.0.0"
description = "One-line description of what the library does."
license = "LicenseName"
dependencies = "Required dependencies or 'None'"
recipe_url = "https://github.com/..."
```

**Guidelines:**
- Use proper TOML strings (double quotes)
- Keep description under 200 characters
- Use official license identifiers when possible

### HTML/Templates

- Do not edit HTML files directly
- Edit `templates/template.html` to change the site template
- CSS is in `templates/sqlite.css`

## Directory Structure

```
recipes/
├── build.py              # Converts TOML + template -> HTML
├── generate_summary.py  # Generates summary.csv from all recipes
├── generate_index.sh    # Generates index.html from CSV
├── Makefile             # Build orchestrator
├── AGENTS.md            # This file
├── templates/           # HTML templates and CSS
│   ├── template.html
│   ├── sqlite.css
│   └── logo.svg
├── recipes/             # Individual library recipes
│   └── [letter]/
│       └── [library-name]/
│           ├── library.toml
│           └── install.sh
└── .github/
    └── workflows/
        └── build.yml    # CI/CD pipeline
```

## Common Tasks

### Adding a New Recipe
1. Create directory: `recipes/<first-letter>/<library-name>/`
2. Create `library.toml` with metadata
3. Create `install.sh` with build script
4. Commit changes (HTML will be generated by CI)

### Modifying Build Process
1. Edit `build.py` for TOML-to-HTML conversion
2. Edit `generate_summary.py` for CSV generation
3. Edit `Makefile` for build orchestration

### Modifying Site Template
Edit `templates/template.html` - uses `{{ title }}` and `{{ content }}` placeholders.

---

**Never generate the html files locally, but only within a github action.**
