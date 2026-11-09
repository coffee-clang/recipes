#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "zeromq-$VERSION"
./configure --prefix="$PREFIX" --without-docs
make -j"$(nproc)"
make install
