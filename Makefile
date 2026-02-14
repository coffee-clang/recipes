TOMLS := $(wildcard recipes/*/*/library.toml)
HTMLS := $(TOMLS:/library.toml=/index.html)

.PHONY: all clean checks

all: checks website

checks:
	python3 ./check_canonical_names.py
	python3 ./check_toml_schema.py

docs/.well-known/packages.json.zstd: docs/.well-known/packages.json
	zstd -19 -o docs/.well-known/packages.json.zstd docs/.well-known/packages.json

docs/.well-known/packages.json: generate_packages.py
	python3 ./generate_packages.py

# This will replace the next two targets when github actions are on ubuntu 26.04
# which has lowdown v2
#
# docs/%.html: %.md templates/template-index.html
# 	lowdown -s --template templates/template-index.html $< -o $@

docs/index.html: index.md templates/template-index.html
	python3 ./build_md.py $< $@ templates/template-index.html

docs/about.html: about.md templates/template-index.html
	python3 ./build_md.py $< $@ templates/template-index.html

%/index.html: %/library.toml templates/template.html
	python3 ./build.py $< $@ templates/template.html

letter_index: templates/template.html
	python3 ./generate_letter_indexes.py

website: docs/index.html docs/about.html letter_index $(HTMLS) docs/.well-known/packages.json.zstd
	rsync -avm --include='*/' --include='*.html' --include='install[-.]*' --exclude='*' recipes/ docs/

clean:
	find recipes -name index.html -delete
	rm -f docs/*.html docs/.well-known/*
