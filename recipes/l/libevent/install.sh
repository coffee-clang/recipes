#!/bin/bash
set -e

SCRATCH="${1:-libevent}"
mkdir -p "$SCRATCH"

URL="https://github.com/libevent/libevent/releases/download/release-2.1.13/libevent-2.1.13.tar.gz"
VERSION="2.1.13"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
