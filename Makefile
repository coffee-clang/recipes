MDS := $(wildcard recipes/*/*/library.toml)
HTMLS := $(MDS:/library.toml=/index.html)

.PHONY: all clean

all: about.html $(HTMLS)

about.html: about.md templates/template.html
	lowdown about.md | sed -e 's/{{ title }}/Cup of Coffee - About/' -e '/{{ content }}/r /dev/stdin' -e '/{{ content }}/d' templates/template.html > $@

%/index.html: %/library.toml templates/template.html
	python3 ./build.py $< $@ templates/template.html

clean:
	find recipes -name index.html -delete
	rm -f about.html
