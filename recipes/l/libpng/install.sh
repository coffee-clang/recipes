#!/bin/bash
set -e

SCRATCH="${1:-libpng}"
mkdir -p "$SCRATCH"

URL="https://sourceforge.net/projects/libpng/files/libpng1.6.46/libpng-1.6.46.tar.gz"
VERSION="1.6.46"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
