#!/bin/bash
set -e

SCRATCH="${1:-util-linux}"
mkdir -p "$SCRATCH"

URL="https://github.com/karelzak/util-linux/archive/refs/tags/v2.40.2.tar.gz"
VERSION="2.40.2"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
