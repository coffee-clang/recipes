#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "zeromq-$VERSION"
./configure --prefix="$PREFIX" --without-docs
make -j"$(nproc)"
make install
