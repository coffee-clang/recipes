#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "nettle-$VERSION"
# nettle defaults to lib64 on 64-bit hosts.
./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --disable-documentation
make -j"$(nproc)"
make install
