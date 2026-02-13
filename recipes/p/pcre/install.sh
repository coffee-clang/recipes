#!/bin/bash
set -e

SCRATCH="${1:-pcre}"
mkdir -p "$SCRATCH"

URL="https://sourceforge.net/projects/pcre/files/pcre/8.45/pcre-8.45.tar.gz"
VERSION="8.45"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
