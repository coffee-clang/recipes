#!/bin/bash
set -e

SCRATCH="${1:-qrencode}"
mkdir -p "$SCRATCH"

URL="https://github.com/fukuchi/libqrencode/archive/refs/tags/v4.1.1.tar.gz"
VERSION="4.1.1"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
