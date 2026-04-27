#!/bin/bash
set -e

SCRATCH="${1:-check}"
mkdir -p "$SCRATCH"

URL="https://github.com/libcheck/check/releases/download/0.15.2/check-0.15.2.tar.gz"
VERSION="0.15.2"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
