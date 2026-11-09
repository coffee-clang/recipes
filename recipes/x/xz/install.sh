#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "xz-$VERSION"
./configure --prefix="$PREFIX" --disable-doc --disable-nls
make -j"$(nproc)"
make install
