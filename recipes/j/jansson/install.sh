#!/bin/bash
set -e

SCRATCH="${1:-jansson}"
mkdir -p "$SCRATCH"

URL="https://github.com/akheron/jansson/releases/download/v2.14/jansson-2.14.tar.gz"
VERSION="2.14"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
