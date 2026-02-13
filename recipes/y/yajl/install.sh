#!/bin/bash
set -e

SCRATCH="${1:-yajl}"
mkdir -p "$SCRATCH"

URL="https://github.com/lloyd/yajl/archive/refs/tags/2.1.0.tar.gz"
VERSION="2.1.0"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
