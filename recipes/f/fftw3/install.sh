#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-fftw3}"
mkdir -p "$SCRATCH"

URL="https://fftw.org/fftw-3.3.10.tar.gz"
VERSION="3.3.10"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
