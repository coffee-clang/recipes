#!/bin/bash

CSV_FILE="summary.csv"
OUTPUT="index.html"

cat >"$OUTPUT" <<'HEAD'
<!DOCTYPE html>
<html lang="en">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<link href="sqlite.css" rel="stylesheet">
<title>Cup of Coffee - C Package Manager</title>
</head>
<body>
<div class="nosearch">
<div class="logo-container">
<img class="logo" src="logo.svg" alt="Cup of Coffee">
<div class="tagline">
<h1>Cup of Coffee</h1>
<p>C Package Manager</p>
</div>
</div>
<div class="menu mainmenu">
<ul>
<li><a href="index.html">Home</a>
<li><a href="a/index.html">Packages</a>
<li><a href="about.html">About</a>
<li><a href="https://github.com/coffee-clang/recipes">GitHub</a>
</ul>
</div>
</div>

<div class="content">

<h1>C Libraries</h1>

<p>A collection of widely used C libraries with installation recipes.</p>

<h2>Packages</h2>

<table>
<thead>
<tr>
<th>Package</th>
<th>Version</th>
<th>License</th>
<th>Last Updated</th>
</tr>
</thead>
<tbody>
HEAD

tail -n +2 "$CSV_FILE" | sed 's/"//g' | while IFS=',' read -r name version link license date; do
	first_letter="${name:0:1}"
	echo "<tr>"
	echo "<td><a href=\"$first_letter/$name/\">$name</a></td>"
	echo "<td>$version</td>"
	echo "<td>$license</td>"
	echo "<td>$date</td>"
	echo "</tr>"
done >>"$OUTPUT"

TOTAL=$(tail -n +2 "$CSV_FILE" | wc -l)

cat >>"$OUTPUT" <<TAIL
</tbody>
</table>

<p>Total: $TOTAL packages</p>

</div>

<p><small><i>This page was last updated on $(date -u +"%Y-%m-%d %H:%M:%SZ")</i></small></p>

</body>
</html>
TAIL

echo "Generated: $OUTPUT"
