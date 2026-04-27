# Add igraph and C Testing Framework Recipes — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add four new widely-used C library recipes (igraph, cmocka, check, unity) to the repository.

**Architecture:** Each recipe is a directory under `recipes/<first-letter>/<name>/` containing `library.toml` (metadata) and `install.sh` (wget + tar extraction script), following the exact existing pattern.

**Tech Stack:** Bash, TOML, Makefile (existing validation + HTML generation).

---

### Task 1: Add igraph Recipe

**Files:**
- Create: `recipes/i/igraph/library.toml`
- Create: `recipes/i/igraph/install.sh`

- [ ] **Step 1: Create recipe directory**

```bash
mkdir -p recipes/i/igraph
```

- [ ] **Step 2: Write library.toml**

```toml
title = "igraph"
version = "0.10.15"
description = "igraph is a C library for complex network analysis and graph theory, with efficient implementations for a wide range of graph algorithms."
license = "GPL-2.0"
dependencies = "None (optional: libxml2, gmp, arpack)"
canonical_name = "igraph"
recipe_url = "https://github.com/igraph/igraph/releases/download/0.10.15/igraph-0.10.15.tar.gz"
```

- [ ] **Step 3: Write install.sh**

```bash
#!/bin/bash
set -e

SCRATCH="${1:-igraph}"
mkdir -p "$SCRATCH"

URL="https://github.com/igraph/igraph/releases/download/0.10.15/igraph-0.10.15.tar.gz"
VERSION="0.10.15"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
```

- [ ] **Step 4: Commit igraph recipe**

```bash
git add recipes/i/igraph/
git commit -m "Add igraph recipe"
```

---

### Task 2: Add cmocka Recipe

**Files:**
- Create: `recipes/c/cmocka/library.toml`
- Create: `recipes/c/cmocka/install.sh`

- [ ] **Step 1: Create recipe directory**

```bash
mkdir -p recipes/c/cmocka
```

- [ ] **Step 2: Write library.toml**

```toml
title = "cmocka"
version = "1.1.7"
description = "cmocka is an elegant unit testing framework for C with support for mock objects. It requires only the standard C library and works on many platforms."
license = "Apache-2.0"
dependencies = "None (standard C library only)"
canonical_name = "cmocka"
recipe_url = "https://git.cryptomilk.org/projects/cmocka.git/snapshot/cmocka-1.1.7.tar.gz"
```

- [ ] **Step 3: Write install.sh**

```bash
#!/bin/bash
set -e

SCRATCH="${1:-cmocka}"
mkdir -p "$SCRATCH"

URL="https://git.cryptomilk.org/projects/cmocka.git/snapshot/cmocka-1.1.7.tar.gz"
VERSION="1.1.7"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
```

- [ ] **Step 4: Commit cmocka recipe**

```bash
git add recipes/c/cmocka/
git commit -m "Add cmocka recipe"
```

---

### Task 3: Add check Recipe

**Files:**
- Create: `recipes/c/check/library.toml`
- Create: `recipes/c/check/install.sh`

- [ ] **Step 1: Create recipe directory**

```bash
mkdir -p recipes/c/check
```

- [ ] **Step 2: Write library.toml**

```toml
title = "check"
version = "0.15.2"
description = "Check is a unit testing framework for C. It features a simple interface for defining unit tests, limiting each test to run in a separate process."
license = "LGPL-2.1"
dependencies = "None (standard C library only)"
canonical_name = "check"
recipe_url = "https://github.com/libcheck/check/releases/download/0.15.2/check-0.15.2.tar.gz"
```

- [ ] **Step 3: Write install.sh**

```bash
#!/bin/bash
set -e

SCRATCH="${1:-check}"
mkdir -p "$SCRATCH"

URL="https://github.com/libcheck/check/releases/download/0.15.2/check-0.15.2.tar.gz"
VERSION="0.15.2"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
```

- [ ] **Step 4: Commit check recipe**

```bash
git add recipes/c/check/
git commit -m "Add check recipe"
```

---

### Task 4: Add unity Recipe

**Files:**
- Create: `recipes/u/unity/library.toml`
- Create: `recipes/u/unity/install.sh`

- [ ] **Step 1: Create recipe directory**

```bash
mkdir -p recipes/u/unity
```

- [ ] **Step 2: Write library.toml**

```toml
title = "unity"
version = "2.6.0"
description = "Unity is a simple, straightforward unit testing framework for C, designed especially for embedded and resource-constrained environments."
license = "MIT"
dependencies = "None (single header or minimal source)"
canonical_name = "unity"
recipe_url = "https://github.com/ThrowTheSwitch/Unity/archive/refs/tags/v2.6.0.tar.gz"
```

- [ ] **Step 3: Write install.sh**

```bash
#!/bin/bash
set -e

SCRATCH="${1:-unity}"
mkdir -p "$SCRATCH"

URL="https://github.com/ThrowTheSwitch/Unity/archive/refs/tags/v2.6.0.tar.gz"
VERSION="2.6.0"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
```

- [ ] **Step 4: Commit unity recipe**

```bash
git add recipes/u/unity/
git commit -m "Add unity recipe"
```

---

### Task 5: Validate All Recipes

**Files:**
- Test: `Makefile` (existing)

- [ ] **Step 1: Run make all to validate**

```bash
make all
```

**Expected output:**
- TOML schema validation passes for all new recipes
- Canonical name uniqueness check passes
- HTML generation completes without errors
- Exit code 0

- [ ] **Step 2: Verify no HTML files are staged**

```bash
git status
```

**Expected:** Only the new recipe directories (`recipes/i/igraph/`, `recipes/c/cmocka/`, `recipes/c/check/`, `recipes/u/unity/`) are listed as new files. No `.html` files are shown as untracked or staged.

- [ ] **Step 3: Final commit (if any fixes needed)**

If `make all` revealed any issues (e.g., TOML formatting, canonical name conflicts), fix them and commit:

```bash
git add -A
git commit -m "Fix validation issues in new recipes"
```

---

## Self-Review

### 1. Spec Coverage

| Spec Requirement | Plan Task |
|------------------|-----------|
| Add igraph recipe | Task 1 |
| Add cmocka recipe | Task 2 |
| Add check recipe | Task 3 |
| Add unity recipe | Task 4 |
| Validate with `make all` | Task 5 |
| No generated HTML committed | Task 5 Step 2 |
| Follow existing patterns | All tasks (exact same structure as existing recipes) |

**No gaps found.**

### 2. Placeholder Scan

- No "TBD", "TODO", "implement later" found.
- No vague "add error handling" or "write tests" steps.
- All code blocks contain complete, copy-pasteable content.
- All file paths are exact.
- All commands include expected output.

**No placeholders found.**

### 3. Type Consistency

- All `library.toml` files use the same field names and ordering as existing recipes (title, version, description, license, dependencies, canonical_name, recipe_url).
- All `install.sh` files use the same variable names and structure as existing recipes (SCRATCH, URL, VERSION, ARCHIVE).
- All `canonical_name` values are valid C identifiers and unique within the repository.

**No inconsistencies found.**
