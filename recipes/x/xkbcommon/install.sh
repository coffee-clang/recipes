#!/bin/bash
set -e

SCRATCH="${1:-xkbcommon}"
mkdir -p "$SCRATCH"

URL="https://github.com/xkbcommon/libxkbcommon/archive/refs/tags/xkbcommon-1.5.0.tar.gz"
VERSION="1.5.0"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
