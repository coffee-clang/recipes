#!/bin/bash
set -e

SCRATCH="${1:-bzip2}"
mkdir -p "$SCRATCH"

URL="https://sourceware.org/pub/bzip2/bzip2-1.0.8.tar.gz"
VERSION="1.0.8"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
