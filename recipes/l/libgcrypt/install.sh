#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xjf "$ARCHIVE" --no-same-owner
cd "libgcrypt-$VERSION"
./configure --prefix="$PREFIX" --disable-doc
make -j"$(nproc)"
make install
