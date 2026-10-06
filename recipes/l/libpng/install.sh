#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-libpng}"
mkdir -p "$SCRATCH"

URL="https://sourceforge.net/projects/libpng/files/libpng1.6.46/libpng-1.6.46.tar.gz"
VERSION="1.6.46"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
