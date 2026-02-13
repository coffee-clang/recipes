#!/bin/bash
set -e

SCRATCH="${1:-cairo}"
mkdir -p "$SCRATCH"

URL="https://www.cairographics.org/releases/cairo-1.18.2.tar.xz"
VERSION="1.18.2"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
