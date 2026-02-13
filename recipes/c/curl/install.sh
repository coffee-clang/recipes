#!/bin/bash
set -e

SCRATCH="${1:-curl}"
mkdir -p "$SCRATCH"

URL="https://curl.se/download/curl-8.11.1.tar.gz"
VERSION="8.11.1"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
