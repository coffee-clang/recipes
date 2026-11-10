#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
mkdir -p "$PREFIX/include"
cp "uthash-$VERSION"/src/*.h "$PREFIX/include/"
