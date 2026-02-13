#!/bin/bash
set -e

SCRATCH="${1:-c-ares}"
mkdir -p "$SCRATCH"

URL="https://c-ares.org/download/c-ares-1.34.4.tar.gz"
VERSION="1.34.4"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
