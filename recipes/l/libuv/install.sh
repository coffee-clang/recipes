#!/bin/bash
set -e

SCRATCH="${1:-libuv}"
mkdir -p "$SCRATCH"

URL="https://dist.libuv.org/dist/v1.49.2/libuv-v1.49.2.tar.gz"
VERSION="1.49.2"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
