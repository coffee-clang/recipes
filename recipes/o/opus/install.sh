#!/bin/bash
set -e

SCRATCH="${1:-opus}"
mkdir -p "$SCRATCH"

URL="https://archive.mozilla.org/pub/opus/opus-1.5.2.tar.gz"
VERSION="1.5.2"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
