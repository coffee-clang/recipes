# Add igraph and C Testing Framework Recipes

## Summary

Add four new widely-used C library recipes to the repository: one graph algorithms library and three C unit testing frameworks.

## New Recipes

### igraph
- **Location:** `recipes/i/igraph/`
- **Type:** Graph algorithms and network analysis library (pure C)
- **Files:** `library.toml`, `install.sh`
- **Rationale:** Widely used for network science, graph algorithms, and complex network analysis. Provides a comprehensive C API.

### cmocka
- **Location:** `recipes/c/cmocka/`
- **Type:** C unit testing framework
- **Files:** `library.toml`, `install.sh`
- **Rationale:** Mature testing framework from the Samba/libcacard ecosystem. Supports mocking, output capture, and test fixtures. Used by many security/crypto projects.

### check
- **Location:** `recipes/c/check/`
- **Type:** C unit testing framework
- **Files:** `library.toml`, `install.sh`
- **Rationale:** Feature-rich framework with multiple assertion types, timeout handling, and fork-based test isolation. Used by numerous GNU/Linux projects.

### unity
- **Location:** `recipes/u/unity/`
- **Type:** C unit testing framework
- **Files:** `library.toml`, `install.sh`
- **Rationale:** Single-header (or minimal) testing framework, extremely popular in embedded and IoT development. Part of the ThrowTheSwitch.org ecosystem.

## Design Decisions

- Follow the existing recipe structure exactly: each recipe is a directory under `recipes/<first-letter>/<name>/` containing `library.toml` and `install.sh`.
- `install.sh` follows the established pattern: `wget` the source tarball, extract it, clean up the archive.
- `library.toml` follows the existing schema (title, version, description, license, dependencies, canonical_name, recipe_url).
- All libraries are pure C libraries usable in C programs.
- No generated HTML files will be committed (per AGENTS.md).

## Success Criteria

1. `make all` passes cleanly (TOML schema validation, canonical name uniqueness, HTML generation).
2. All four recipes validate against the existing TOML schema.
3. All canonical names are unique across the repository.
4. No generated `.html` files are added to git.
