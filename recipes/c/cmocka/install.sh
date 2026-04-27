#!/bin/bash
set -e

SCRATCH="${1:-cmocka}"
mkdir -p "$SCRATCH"

URL="https://git.cryptomilk.org/projects/cmocka.git/snapshot/cmocka-1.1.7.tar.gz"
VERSION="1.1.7"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
