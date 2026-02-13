#!/bin/bash
set -e

SCRATCH="${1:-flac}"
mkdir -p "$SCRATCH"

URL="https://downloads.xiph.org/flac/flac-1.4.3.tar.xz"
VERSION="1.4.3"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
