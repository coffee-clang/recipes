TOMLS := $(wildcard recipes/*/*/library.toml)

.PHONY: all clean checks website

all: checks website

checks:
	python3 ./check_canonical_names.py
	python3 ./check_toml_schema.py

# Generate mdBook source files from TOML recipes
src/SUMMARY.md: generate_mdbook_src.py $(TOMLS)
	python3 ./generate_mdbook_src.py

# Build the site with mdBook (reads from src/, writes to docs/)
website: src/SUMMARY.md
	mdbook build
	mkdir -p docs/.well-known
	python3 ./generate_packages.py
	zstd -19 -o docs/.well-known/packages.json.zstd docs/.well-known/packages.json

clean:
	rm -rf src/
	rm -f docs/*.html docs/*.css docs/*.json docs/*.js docs/*.svg docs/*.png docs/searcher.js docs/highlight.js docs/book.js docs/clipboard.min.js docs/elasticlunr.min.js docs/mark.min.js docs/print.html
	rm -rf docs/css/ docs/FontAwesome/ docs/fonts/ docs/.well-known/