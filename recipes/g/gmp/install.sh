#!/bin/bash
set -e

SCRATCH="${1:-gmp}"
mkdir -p "$SCRATCH"

URL="https://ftp.gnu.org/gnu/gmp/gmp-6.3.0.tar.gz"
VERSION="6.3.0"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
