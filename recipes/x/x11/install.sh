#!/bin/bash
set -e

SCRATCH="${1:-x11}"
mkdir -p "$SCRATCH"

URL="https://x.org/archive/individual/lib/libX11-1.8.9.tar.xz"
VERSION="1.8.9"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
