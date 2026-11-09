#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
mkdir -p "$PREFIX/include"
cp "uthash-$VERSION"/src/*.h "$PREFIX/include/"
