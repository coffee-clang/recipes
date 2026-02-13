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
	fi

	license="Unknown"
	case "$library_name" in
	zlib) license="zlib" ;;
	openssl) license="Apache-2.0" ;;
	sqlite) license="Public Domain" ;;
	glib | atk | pango | harfbuzz) license="LGPL-2.1" ;;
	gtk) license="LGPL-2.1" ;;
	ncurses) license="MIT" ;;
	curl | libcurl) license="curl" ;;
	libpng) license="libpng" ;;
	freetype) license="FreeType" ;;
	expat) license="MIT" ;;
	pcre | pcre2) license="BSD" ;;
	gsl) license="GPL-3.0" ;;
	gmp | mpfr) license="LGPL-3.0" ;;
	nettle) license="LGPL-2.1" ;;
	xz | liblzma) license="Public Domain" ;;
	bzip2) license="bzip2" ;;
	lz4) license="BSD-2-Clause" ;;
	zstd | brotli) license="BSD-3-Clause" ;;
	fftw3) license="GPL-2.0" ;;
	lmdb) license="OpenSSL" ;;
	json-c | jansson | cjson | yajl) license="MIT" ;;
	libuv | libevent) license="MIT" ;;
	zeromq) license="LGPL-3.0" ;;
	opus | speex | flac | wavpack) license="BSD-3-Clause" ;;
	ffmpeg) license="GPL-3.0" ;;
	cunit) license="GPL-2.0" ;;
	mesa | drm | pixman) license="MIT" ;;
	dbus) license="GPL-2.0" ;;
	alsa-lib) license="LGPL-2.1" ;;
	acl | attr) license="LGPL-2.1" ;;
	cairo) license="LGPL-2.1" ;;
	libxml2 | libxslt) license="MIT" ;;
	readline) license="GPL-3.0" ;;
	opus) license="BSD-3-Clause" ;;
	tiff) license="MIT" ;;
	icu) license="Unicode" ;;
	esac

	last_updated=$(stat -c %y "$mdfile" 2>/dev/null | cut -d' ' -f1 || stat -f %Sm -t %Y-%m-%d "$mdfile")

	echo "\"$library_name\",\"$version\",\"$link\",\"$license\",\"$last_updated\""

done >>"$OUTPUT"

echo "Summary written to $OUTPUT"
