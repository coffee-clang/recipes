#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
mkdir -p "$PREFIX/include"
# A single-file library: the .c file is also its header.
cp "wuffs-$VERSION/release/c/wuffs-v0.3.c" "$PREFIX/include/"
