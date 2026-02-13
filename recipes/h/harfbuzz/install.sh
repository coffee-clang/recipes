#!/bin/bash
set -e

SCRATCH="${1:-harfbuzz}"
mkdir -p "$SCRATCH"

URL="https://github.com/harfbuzz/harfbuzz/releases/download/10.0.1/harfbuzz-10.0.1.tar.xz"
VERSION="10.0.1"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
