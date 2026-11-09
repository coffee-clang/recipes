#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "libmicrohttpd-$VERSION"
./configure --prefix="$PREFIX" --disable-doc --disable-examples
make -j"$(nproc)"
make install
