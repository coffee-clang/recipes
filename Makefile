MDS := $(wildcard [a-z]/*/index.md)
HTMLS := $(MDS:.md=.html)

.PHONY: all clean

all: $(HTMLS)

%/index.html: %/index.md templates/template.html
	./build.sh $< $@ templates/template.html

clean:
	rm -f [a-z]/*/index.html
