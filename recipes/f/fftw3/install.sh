#!/bin/bash
set -e

SCRATCH="${1:-fftw3}"
mkdir -p "$SCRATCH"

URL="https://fftw.org/fftw-3.3.10.tar.gz"
VERSION="3.3.10"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
