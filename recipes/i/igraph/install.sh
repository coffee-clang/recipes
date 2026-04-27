#!/bin/bash
set -e

SCRATCH="${1:-igraph}"
mkdir -p "$SCRATCH"

URL="https://github.com/igraph/igraph/releases/download/0.10.15/igraph-0.10.15.tar.gz"
VERSION="0.10.15"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
