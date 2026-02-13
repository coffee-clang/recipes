#!/bin/bash
set -e

SCRATCH="${1:-libxslt}"
mkdir -p "$SCRATCH"

URL="https://download.gnome.org/sources/libxslt/${VERSION%.*}/libxslt-1.1.42.tar.gz"
VERSION="1.1.42"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
