#!/bin/bash
set -e

SCRATCH="${1:-xz}"
mkdir -p "$SCRATCH"

URL="https://tukaani.org/xz/xz-5.6.3.tar.gz"
VERSION="5.6.3"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
