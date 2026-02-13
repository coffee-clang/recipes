#!/bin/bash
set -e

INPUT="index.md"
OUTPUT="index.html"
TEMPLATE="templates/template.html"

CONTENT=$(lowdown "$INPUT")

ALPHABET="A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"

LETTER_TABLE="<h2>Browse by Letter</h2><p>"
for letter in $ALPHABET; do
	lower=$(echo "$letter" | tr '[:upper:]' '[:lower:]')
	if [ -d "recipes/$lower" ] && [ "$(ls "recipes/$lower"/*/library.toml 2>/dev/null | wc -l)" -gt 0 ]; then
		LETTER_TABLE+="<a href=\"recipes/$lower/index.html\">$letter</a> "
	else
		LETTER_TABLE+="$letter "
	fi
done
LETTER_TABLE+="</p>"

FULL_CONTENT="$CONTENT $LETTER_TABLE"

sed -e "s/{{ title }}/Cup of Coffee/g" \
	-e "/{{ content }}/r /dev/stdin" \
	-e "/{{ content }}/d" \
	"$TEMPLATE" >"$OUTPUT" <<EOF
$FULL_CONTENT
EOF

echo "Generated: $OUTPUT"
