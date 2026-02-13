#!/bin/bash

CSV_FILE="summary.csv"
OUTPUT="index.md"

cat >"$OUTPUT" <<'HEADER'
# C Libraries

A collection of widely used C libraries with installation recipes.

## Packages

| Package | Version | License | Last Updated | Link |
|---------|---------|---------|--------------|------|
HEADER

tail -n +2 "$CSV_FILE" | while IFS=',' read -r name version link license date; do
    first_letter="${name:0:1}"
    echo "| [$name]($first_letter/$name/) | $version | $license | $date | $link |"
done >>"$OUTPUT"

echo "" >>"$OUTPUT"
echo "Total: $(tail -n +2 "$CSV_FILE" | wc -l) packages" >>"$OUTPUT"

lowdown -s <"$OUTPUT" >"${OUTPUT%.md}.html"

echo "Generated: $OUTPUT and index.html"
