# AGENTS.md

Behavioral guidelines for this repository.

## Behavioral Guidelines

- **Think before coding:** State assumptions explicitly. Ask if unclear.
- **Simplicity first:** Minimum code that solves the problem. No speculative features.
- **Surgical changes:** Touch only what you must. Don't "improve" unrelated code.
- **Goal-driven:** Define success criteria before implementing.

---

## Project Overview

This repository contains recipes for building C libraries. Each recipe has:
- `library.toml` - metadata (title, version, license, dependencies, recipe_url)
- `install.sh` - install script *template*; the published script is rendered from it

The build system generates HTML documentation from these recipes using mdBook.

Read carefully the README.md file for additional instructions to follow.

## Build Commands

```bash
make all    # Runs tests + all three checkers, then builds docs/ via mdBook
make site   # Builds docs/ without the checks (escape hatch for a lint failure)
make clean  # Removes all generated files (src/, docs/)
```

**Never generate HTML files locally.** Only generate them within GitHub Actions. Keep generated HTML files (.html) out of git commits.

**The build pipeline:**
1. `test` - Unit tests (`python3 -m unittest discover -p 'test_*.py'`)
2. `check_canonical_names.py` - Validate no duplicate canonical names
3. `check_toml_schema.py` - Validate TOML schema
4. `check_dependencies.py` - Validate every dependency resolves
5. `generate_mdbook_src.py` - Generate `src/` from TOML recipes (markdown pages, SUMMARY.md, and each published `install.sh` rendered from its template)
6. `mdbook build` - Convert `src/` markdown to `docs/` HTML
7. `generate_packages.py` - Write per-recipe JSON + `docs/.well-known/packages.json`

**Important files:**
- `recipe_metadata.py` - Shared recipe discovery, naming, and dependency parsing. All checkers and generators import from it; do not re-implement these locally.
- `book.toml` - mdBook configuration (root of project)
- `theme/index.hbs` - Custom mdBook template (uses remote CSS from coffee-clang.github.io)
- `src/SUMMARY.md` - Auto-generated table of contents (from `generate_mdbook_src.py`)
- `src/<letter>/<name>/index.md` - Auto-generated recipe pages
- `src/<letter>/index.md` - Auto-generated letter index pages

## Design: Remote CSS via Brand Identity

This site reuses the **coffee-clang brand identity** via remote CSS imports from the main site (`https://coffee-clang.github.io/`):

- **`normalize.css`** — CSS reset
- **`brand.css`** — Shared brand identity (coffee color palette, fonts, layout)
- **`mdbook.css`** — mdBook-specific overrides (sidebar, menu bar, search, tables)
- The `logo.svg` entry is historical: the asset is no longer in the tree. `index.md` and `theme/index.hbs` both load it from `coffee-clang.github.io`

No local CSS or static assets are needed — everything is loaded remotely from the main site. The `theme/index.hbs` template includes these imports in the `<head>`.

## Code Style

### Python
- Stdlib only (`tomllib`, `subprocess`, `os`, `pathlib`, `sys`)
- 4-space indentation, 88-char max line length
- Use f-strings, explicit imports, type hints where beneficial

### Shell
- Use `#!/bin/bash` or `#!/usr/bin/env bash`
- Always use `set -e` for error handling
- Quote variables: `"$VAR"`, use `${VAR}` in strings

### TOML Recipe Files
```toml
title = "PackageName"
version = "1.0.0"
description = "One-line description."
license = "LicenseName"
canonical_name = "package_name"
recipe_url = "https://..."  # a release archive, never a git URL
sha256 = "..."            # 64 lowercase hex digits, checked before extraction
sha256_source = "upstream"  # signature | upstream | tofu, see ARCHITECTURE.md
output_type = "library"   # library | executable | both | data
libname = "z"             # -lz; a list for several libraries
# header_only = true      # instead of libname, for header-only packages
# include_dir = "include/sub"  # optional, relative to the prefix; default include
# lib_dir = "lib"         # optional, relative to the prefix; default lib
# notes = "..."           # optional usage advice, e.g. an implementation macro

[dependencies]            # registry libraries only
zlib = ""                 # Empty value means "any version"
openssl = ">=1.1"

[build-dependencies]      # host tools only, from HOST_TOOLS
cmake = ""
```
- Use double quotes, keep description under 200 chars
- `dependencies` is a **table only**. An empty table means "no dependencies"; a string form is rejected by `check_toml_schema.py`.
- `[dependencies]` names registry libraries; `[build-dependencies]` names host tools from `HOST_TOOLS` in `check_dependencies.py`. A tool under `[dependencies]` is rejected.
- A `library`/`both` recipe must set `libname` or `header_only = true`.
- `canonical_name` must be a valid C identifier (underscores, no dashes) and unique. The directory name is registered as an alias, so it may keep the upstream dashed spelling.
- `title` is used as a JSON filename, so it must not contain `/`, `\`, or `..`
- A `description`/`license` value is rendered into a Markdown table; the generator escapes `|` for you

## Directory Structure

```
recipes/
├── recipe_metadata.py              # Shared recipe discovery + parsing helpers
├── generate_mdbook_src.py          # Generates src/ from TOML recipes
├── generate_packages.py            # Generates packages.json
├── check_canonical_names.py        # Validate unique names
├── check_toml_schema.py            # Validate TOML schema
├── check_dependencies.py           # Validate dependency resolution
├── test_*.py                       # Unit tests, one module per checker
├── Makefile                        # Build orchestrator
├── AGENTS.md                       # This file
├── book.toml                       # mdBook configuration
├── index.md, about.md              # Page sources (copied into src/)
├── theme/
│   └── index.hbs                   # Custom mdBook template (remote CSS)
├── LICENSE, README.md, .gitignore
├── src/                            # mdBook source (generated, gitignored)
│   ├── SUMMARY.md                  # Auto-generated table of contents
│   ├── index.md, about.md          # Copied from root
│   ├── [letter]/
│   │   ├── index.md                # Letter index page
│   │   └── [library-name]/
│   │       ├── index.md            # Recipe page
│   │       └── install.sh          # Rendered from the recipe's template
├── recipes/                        # Library recipes (source of truth)
│   └── [letter]/
│       └── [library-name]/
│           ├── library.toml
│           └── install.sh
├── docs/                           # Generated output (deployed, gitignored)
└── .github/
    └── workflows/
        ├── build.yml               # Build & deploy to GitHub Pages
        └── check.yml               # Validate TOML on PRs
```

## Common Tasks

### Adding a New Recipe
1. Create `recipes/<letter>/<name>/`
2. Add `library.toml` with metadata
3. Add an `install.sh` template following the contract in README.md: the
   lines `#!/bin/bash` and `set -e -o pipefail -u`, then a body that reads
   `$PACKAGE`, `$VERSION`, `$ARCHIVE` and `$PREFIX` (never assigns them),
   extracts the already verified `$ARCHIVE`, builds in the current scratch
   directory and installs into `$PREFIX`. It never downloads anything. Extract with
   `tar <op> "$ARCHIVE" --no-same-owner` — the flag goes *after* the archive,
   because `f` takes the next argument as its filename.
4. `chmod +x install.sh`; `test_install_script_execution.py` fails if it is not
5. Commit (HTML generated by CI)

### Fixing Recipe Metadata

Every template must install into `$PREFIX`
(`test_install_scripts.py::TestInstallContract`). There is no fetch-only
exemption: a recipe that cannot build yet is a failing test, not a skip.

---

## Coding Mode

You are in **coding mode**. Follow Test-Driven Development for every change. Do not skip or reorder steps.

**Announce at start:** "I'm using the code prompt. I will implement this step by step using TDD."

## Process

1. **Understand** — ask clarifying questions until the request is clear. Confirm acceptance criteria.
2. **Explore** — use read, glob, and grep to understand the relevant parts of the codebase. Note the testing framework, linting, and build system.
3. **Write a failing test** — the minimal test expressing the desired behavior. Match project conventions.
4. **Run it** — confirm it fails with a clear error. Show the output.
5. **Write minimal implementation** — the simplest code to pass the test. No extra features, no premature abstraction.
6. **Run again** — confirm it passes. Show the output.
7. **Verify** — run linters, type checkers, and the full test suite. Fix all failures before moving on.
8. **Review** — re-read your changes. Check for edge cases, naming consistency, and unrelated changes.

## Conventions

- Follow existing code patterns (style, naming, imports, error handling, file organization).
- Do not introduce new dependencies without asking.
- Do not restructure code unless it is part of the agreed task.
- Ask one question at a time. Prefer multiple-choice.
- Stop and ask if a task would take more than 30 minutes.

**Use Markdown lists for all structured information. Markdown tables are prohibited.**

## Tool Usage

- **read** — before editing any file.
- **write** — new files or complete rewrites only.
- **edit** — prefer for small, targeted changes to existing files.
- **bash** — for tests, linters, git, builds. Not for file operations.
- **grep** — for finding symbols, definitions, imports.
- **glob** — for finding files by name pattern.
- **list_dir** — for exploring the project structure.

## System Intervention

If a task requires intervening on the system itself (e.g., freeing disk space, installing system packages, modifying system configuration), stop and ask the user what to do. Do not take system-level actions autonomously.
