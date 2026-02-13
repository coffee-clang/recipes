#!/bin/bash
set -e

SCRATCH="${1:-attr}"
mkdir -p "$SCRATCH"

URL="https://download.savannah.nongnu.org/releases/attr/attr-2.5.2.tar.gz"
VERSION="2.5.2"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
