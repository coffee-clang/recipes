#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "libogg-$VERSION"
./configure --prefix="$PREFIX"
make -j"$(nproc)"
make install
