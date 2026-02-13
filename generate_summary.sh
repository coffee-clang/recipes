#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT="$SCRIPT_DIR/summary.csv"

echo "library_name,version,link,license,last_updated" >"$OUTPUT"

find "$SCRIPT_DIR/recipes" -name "index.md" -type f | while read -r mdfile; do
    dir=$(dirname "$mdfile")

    library_name=$(basename "$dir")

    version=$(grep -A1 "^## Version" "$mdfile" | tail -1 | tr -d ' ')

    link=""
    if grep -q "https://" "$mdfile"; then
        link=$(grep -o 'https://[^ )]*' "$mdfile" | head -1)
    else
        link=""
    fi

    if grep -q "^## License" "$mdfile"; then
        license=$(awk '/^## License/,/^[^#]/ {if (!/^## License/ && !/^#/) print}' "$mdfile" | head -1 | tr -d ' ')
    else
        license="Unknown"
    fi

    last_updated=$(stat -c %y "$mdfile" 2>/dev/null | cut -d' ' -f1 || stat -f %Sm -t %Y-%m-%d "$mdfile")

    echo "\"$library_name\",\"$version\",\"$link\",\"$license\",\"$last_updated\""

done | sort >>"$OUTPUT"

echo "Summary written to $OUTPUT"
