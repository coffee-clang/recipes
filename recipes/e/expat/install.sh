#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "expat-$VERSION"
./configure --prefix="$PREFIX" --without-docbook
make -j"$(nproc)"
make install
