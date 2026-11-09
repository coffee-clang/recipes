#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "acl-$VERSION"
./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j"$(nproc)"
make install
