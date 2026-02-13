#!/bin/bash
set -e

SCRATCH="${1:-berkeley-db}"
mkdir -p "$SCRATCH"

URL="https://download.oracle.com/berkeley-db/db-6.2.32.tar.gz"
VERSION="6.2.32"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
