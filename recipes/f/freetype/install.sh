#!/bin/bash
set -e

SCRATCH="${1:-freetype}"
mkdir -p "$SCRATCH"

URL="https://download.savannah.nongnu.org/releases/freetype/freetype-2.13.3.tar.gz"
VERSION="2.13.3"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
