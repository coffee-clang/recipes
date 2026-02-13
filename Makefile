MDS := $(wildcard recipes/*/*/index.md)
HTMLS := $(MDS:.md=.html)

.PHONY: all clean

all: $(HTMLS)

%/index.html: %/index.md templates/template.html
	./build.sh $< $@ templates/template.html

clean:
	find recipes -name index.html -delete
