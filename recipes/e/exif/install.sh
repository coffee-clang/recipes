#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xjf "$ARCHIVE" --no-same-owner
cd "libexif-$VERSION"
./configure --prefix="$PREFIX" --disable-docs --disable-nls
make -j"$(nproc)"
make install
