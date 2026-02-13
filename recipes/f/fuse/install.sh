#!/bin/bash
set -e

SCRATCH="${1:-fuse}"
mkdir -p "$SCRATCH"

URL="https://github.com/libfuse/libfuse/releases/download/fuse-3.16.2/fuse-3.16.2.tar.gz"
VERSION="3.16.2"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
