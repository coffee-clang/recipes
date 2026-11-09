#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "nghttp2-$VERSION"
./configure --prefix="$PREFIX" --enable-lib-only
make -j"$(nproc)"
make install
