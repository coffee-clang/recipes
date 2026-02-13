#!/bin/bash
set -e

SCRATCH="${1:-fribidi}"
mkdir -p "$SCRATCH"

URL="https://github.com/fribidi/fribidi/releases/download/v1.0.16/fribidi-1.0.16.tar.gz"
VERSION="1.0.16"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
