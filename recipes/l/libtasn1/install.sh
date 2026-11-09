#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "libtasn1-$VERSION"
./configure --prefix="$PREFIX" --disable-doc
make -j"$(nproc)"
make install
