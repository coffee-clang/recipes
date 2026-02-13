#!/bin/bash

CSV_FILE="summary.csv"
OUTPUT="index.md"

cat >"$OUTPUT" <<'HEADER'
# C Libraries

A collection of widely used C libraries with installation recipes.

## Packages

| Package | Version | License | Last Updated |
|---------|---------|---------|--------------|
HEADER

tail -n +2 "$CSV_FILE" | while IFS=',' read -r name version link license date; do
  name=$(echo "$name" | tr -d '"')
  version=$(echo "$version" | tr -d '"')
  license=$(echo "$license" | tr -d '"')
  date=$(echo "$date" | tr -d '"')

  first_letter="${name:0:1}"
  echo "| [$name](recipes/$first_letter/$name/) | $version | $license | $date |"
done >>"$OUTPUT"

echo "" >>"$OUTPUT"
echo "Total: $(tail -n +2 "$CSV_FILE" | wc -l) packages" >>"$OUTPUT"

lowdown -s <"$OUTPUT" >"${OUTPUT%.md}.html"

echo "Generated: $OUTPUT and index.html"
