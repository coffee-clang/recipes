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

# docs/%.html: %.md templates/template-index.html
# 	lowdown -s --template templates/template-index.html $< -o $@

docs/index.html: index.md templates/template-index.html
	@title=$$(sed -n 's/^title: //p' index.md) && \
	lowdown -s index.md | sed -n '/<body>/,/<\/body>/p' | sed '1d;$$d' > /tmp/body.html && \
	sed -e "s/\\$$title/$$title/" -e "/\\$$body/r /tmp/body.html" -e "/\\$$body/d" templates/template-index.html > $$@

docs/about.html: about.md templates/template-index.html
	@title=$$(sed -n 's/^title: //p' about.md) && \
	lowdown -s about.md | sed -n '/<body>/,/<\/body>/p' | sed '1d;$$d' > /tmp/body.html && \
	sed -e "s/\\$$title/$$title/" -e "/\\$$body/r /tmp/body.html" -e "/\\$$body/d" templates/template-index.html > $$@

%/index.html: %/library.toml templates/template.html
	python3 ./build.py $< $@ templates/template.html

letter_index: templates/template.html
	python3 ./generate_letter_indexes.py

website: docs/index.html docs/about.html letter_index $(HTMLS) docs/.well-known/packages.json.zstd
	rsync -avm --include='*/' --include='*.html' --include='install[-.]*' --exclude='*' recipes/ docs/

clean:
	find recipes -name index.html -delete
	rm -f docs/*.html docs/.well-known/*
