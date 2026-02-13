#!/bin/bash
set -e

INPUT="$1"
OUTPUT="$2"
TEMPLATE="$3"

TITLE=$(head -n1 "$INPUT" | sed 's/Title: //')
DIR=$(dirname "$INPUT")

LAST_UPDATED=$(git -C "$DIR" log -1 --format=%cd --date=format:"%Y-%m-%d" HEAD 2>/dev/null) ||
	LAST_UPDATED=$(date -r "$INPUT" +"%Y-%m-%d" 2>/dev/null) ||
	LAST_UPDATED=$(date +"%Y-%m-%d")

CONTENT=$(tail -n +4 "$INPUT")

REORDERED=$(echo "$CONTENT" | awk '
/^## Recipe/ { in_recipe = 1 }
/^## / && !in_recipe { 
    section = $0
    next
}
in_recipe {
    recipe = recipe $0 "\n"
    next
}
section != "" {
    sections[section] = sections[section] $0 "\n"
    next
}
{ 
    sections[""] = sections[""] $0 "\n"
}
END {
    # Print Description
    if ("" in sections) print sections[""]
    # Print Version
    if ("## Version" in sections) print "## Version\n" sections["## Version"]
    # Print License
    if ("## License" in sections) print "## License\n" sections["## License"]
    # Print Dependencies
    if ("## Dependencies" in sections) print "## Dependencies\n" sections["## Dependencies"]
    # Print Recipe
    if (recipe != "") print "## Recipe\n" recipe
}
')

{
	echo "$REORDERED"
	echo ""
	echo "## Last Update"
	echo "$LAST_UPDATED"
} | lowdown >"$OUTPUT.tmp"

sed -e "s/{{ title }}/${TITLE}/g" \
	-e "/{{ content }}/{
        r $OUTPUT.tmp
        d
    }" "$TEMPLATE" >"$OUTPUT"

rm -f "$OUTPUT.tmp"
