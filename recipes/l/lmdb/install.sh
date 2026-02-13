#!/bin/bash
set -e

SCRATCH="${1:-lmdb}"
mkdir -p "$SCRATCH"

URL="https://github.com/LMDB/lmdb/archive/refs/tags/LMDB_0.9.33.tar.gz"
VERSION="0.9.33"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
