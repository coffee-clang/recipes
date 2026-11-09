#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xJf "$ARCHIVE" --no-same-owner
cd "xtrans-$VERSION"
./configure --prefix="$PREFIX" --disable-docs
make -j"$(nproc)"
make install
