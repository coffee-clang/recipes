#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "openssl-$VERSION"
./Configure --prefix="$PREFIX" --libdir=lib shared no-docs
make -j"$(nproc)"
make install
