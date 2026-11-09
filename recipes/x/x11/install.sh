#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xJf "$ARCHIVE" --no-same-owner
cd "libX11-$VERSION"
./configure --prefix="$PREFIX" --disable-specs
make -j"$(nproc)"
make install
