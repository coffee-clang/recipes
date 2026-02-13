#!/bin/bash
set -e

SCRATCH="${1:-pango}"
mkdir -p "$SCRATCH"

URL="https://download.gnome.org/sources/pango/${VERSION%.*}/pango-1.54.0.tar.xz"
VERSION="1.54.0"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
