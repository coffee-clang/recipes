#!/bin/bash
set -e

SCRATCH="${1:-mpfr}"
mkdir -p "$SCRATCH"

URL="https://ftp.gnu.org/gnu/mpfr/mpfr-4.2.1.tar.gz"
VERSION="4.2.1"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
