#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "simde-$VERSION"
# Header-only library.
mkdir -p "$PREFIX/include"
cp -r simde "$PREFIX/include/"
