#!/bin/bash
set -e

SCRATCH="${1:-sqlite}"
mkdir -p "$SCRATCH"

URL="https://www.sqlite.org/2024/sqlite-autoconf-3.47.2.tar.gz"
VERSION="3.47.2"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
