MDS := $(wildcard recipes/*/*/library.toml)
HTMLS := $(MDS:/library.toml=/index.html)

.PHONY: all clean letter_index

all: index.html about.html letter_index $(HTMLS)

index.html: index.md templates/template.html
	./generate_index.sh

about.html: about.md templates/template.html
	lowdown about.md | sed -e 's/{{ title }}/Cup of Coffee - About/' -e '/{{ content }}/r /dev/stdin' -e '/{{ content }}/d' templates/template.html > $@

letter_index: templates/template.html
	python3 ./generate_letter_indexes.py

%/index.html: %/library.toml templates/template.html
	python3 ./build.py $< $@ templates/template.html

clean:
	find recipes -name index.html -delete
	rm -f index.html about.html
