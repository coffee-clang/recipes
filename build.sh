#!/bin/bash
set -e

INPUT="$1"
OUTPUT="$2"
TEMPLATE="$3"

TITLE=$(head -n1 "$INPUT" | sed 's/Title: //')

tail -n +4 "$INPUT" | lowdown >"$OUTPUT.tmp"

sed -e "s/{{ title }}/${TITLE}/g" \
	-e "/{{ content }}/{
        r $OUTPUT.tmp
        d
    }" "$TEMPLATE" >"$OUTPUT"

rm -f "$OUTPUT.tmp"
