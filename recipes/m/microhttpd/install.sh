#!/bin/bash
set -e

SCRATCH="${1:-microhttpd}"
mkdir -p "$SCRATCH"

URL="https://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-1.0.0.tar.gz"
VERSION="1.0.0"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
