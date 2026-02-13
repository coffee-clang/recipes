#!/bin/bash
set -e

SCRATCH="${1:-zlib}"
mkdir -p "$SCRATCH"

URL="https://github.com/madler/zlib/archive/refs/tags/v1.3.1.tar.gz"
VERSION="1.3.1"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
