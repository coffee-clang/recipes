TOMLS := $(wildcard recipes/*/*/library.toml)
SCRIPTS := $(wildcard recipes/*/*/install.sh)
PYTHON := python3

# Everything a generated page depends on. SCRIPTS matters as much as TOMLS:
# without it an edited install.sh leaves src/SUMMARY.md newer than its inputs,
# make skips the generator, and mdbook republishes the stale script.
GEN_DEPS := generate_mdbook_src.py recipe_metadata.py recipe_script.py $(TOMLS) $(SCRIPTS)

# A failed generator must not leave a half-written SUMMARY.md behind looking
# up to date, or the next build republishes it.
.DELETE_ON_ERROR:

.PHONY: all clean checks test site website

all: checks website

checks: test
	$(PYTHON) ./check_canonical_names.py
	$(PYTHON) ./check_toml_schema.py
	$(PYTHON) ./check_dependencies.py

test:
	$(PYTHON) -m unittest discover -p 'test_*.py' -v

src/SUMMARY.md: $(GEN_DEPS)
	$(PYTHON) ./generate_mdbook_src.py

# Build the site with mdBook (reads from src/, writes to docs/)
website: src/SUMMARY.md
	mdbook build
	mkdir -p docs/.well-known
	$(PYTHON) ./generate_packages.py
	zstd -12 -o docs/.well-known/packages.json.zstd docs/.well-known/packages.json

# Publish without linting first, so a metadata lint failure can never block a
# site rebuild. CI runs `all`, which does both.
site: website

clean:
	rm -rf src/ docs/
