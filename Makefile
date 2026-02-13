MDS := $(wildcard recipes/*/*/library.toml)
HTMLS := $(MDS:/library.toml=/index.html)

.PHONY: all clean

all: $(HTMLS)

%/index.html: %/library.toml templates/template.html
	python3 ./build.py $< $@ templates/template.html

clean:
	find recipes -name index.html -delete
