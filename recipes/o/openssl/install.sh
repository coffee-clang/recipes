#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "openssl-$VERSION"
./Configure --prefix="$PREFIX" --libdir=lib shared no-docs
make -j"$(nproc)"
make install
