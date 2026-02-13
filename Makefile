TOMLS := $(wildcard recipes/*/*/library.toml)
HTMLS := $(TOMLS:/library.toml=/index.html)

.PHONY: all clean letter_index packages.json.zstd

all: index.html about.html letter_index $(HTMLS) packages.json.zstd

packages.json.zstd: packages.json
	zstd -19 -o docs/.well-known/packages.json.zstd packages.json

packages.json: generate_packages.py
	python3 ./generate_packages.py

index.html: index.md templates/template.html
	lowdown index.md | sed -e 's/{{ title }}/Cup of Coffee/' -e '/{{ content }}/r /dev/stdin' -e '/{{ content }}/d' templates/template.html > $@

about.html: about.md templates/template.html
	lowdown about.md | sed -e 's/{{ title }}/Cup of Coffee - About/' -e '/{{ content }}/r /dev/stdin' -e '/{{ content }}/d' templates/template.html > $@

letter_index: templates/template.html
	python3 ./generate_letter_indexes.py

%/index.html: %/library.toml templates/template.html
	python3 ./build.py $< $@ templates/template.html

html: all
	cp *.html docs/
	rsync -avm --include='*/' --include='*.html' --exclude='*' recipes/ docs/

clean:
	find recipes -name index.html -delete
	rm -f index.html about.html
