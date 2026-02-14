TOMLS := $(wildcard recipes/*/*/library.toml)
HTMLS := $(TOMLS:/library.toml=/index.html)

.PHONY: all clean check_canonical_names

all: check_canonical_names website

check_canonical_names:
	python3 ./check_canonical_names.py

docs/.well-known/packages.json.zstd: docs/.well-known/packages.json
	zstd -19 -o docs/.well-known/packages.json.zstd docs/.well-known/packages.json

docs/.well-known/packages.json: generate_packages.py
	python3 ./generate_packages.py

index.html: index.md templates/template.html
	lowdown index.md | sed -e 's/{{ title }}/Cup of Coffee/' -e '/{{ content }}/r /dev/stdin' -e '/{{ content }}/d' templates/template.html > $@

about.html: about.md templates/template.html
	lowdown about.md | sed -e 's/{{ title }}/Cup of Coffee - About/' -e '/{{ content }}/r /dev/stdin' -e '/{{ content }}/d' templates/template.html > $@

%/index.html: %/library.toml templates/template.html
	python3 ./build.py $< $@ templates/template.html

website: index.html about.html $(HTMLS) docs/.well-known/packages.json.zstd
	cp *.html docs/
	rsync -avm --include='*/' --include='*.html' --include='install[-.]*' --exclude='*' recipes/ docs/

clean:
	find recipes -name index.html -delete
	rm -f index.html about.html docs/.well-known/*
