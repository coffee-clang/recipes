#!/bin/bash
set -e

SCRATCH="${1:-expat}"
mkdir -p "$SCRATCH"

URL="https://github.com/libexpat/libexpat/releases/download/R_${VERSION//./_}/expat-2.6.4.tar.gz"
VERSION="2.6.4"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
