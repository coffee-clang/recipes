#!/bin/bash
set -e

SCRATCH="${1:-exif}"
mkdir -p "$SCRATCH"

URL="https://github.com/libexif/libexif/releases/download/v0.6.24/libexif-0.6.24.tar.gz"
VERSION="0.6.24"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
