#!/bin/bash
set -e

SCRATCH="${1:-sds}"
mkdir -p "$SCRATCH"

URL="https://github.com/antirez/sds/archive/refs/tags/2.0.0.tar.gz"
VERSION="2.0.0"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
