#!/bin/bash
set -e

SCRATCH="${1:-nettle}"
mkdir -p "$SCRATCH"

URL="https://ftp.gnu.org/gnu/nettle/nettle-3.10.tar.gz"
VERSION="3.10"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
