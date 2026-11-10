#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "libev-$VERSION"
./configure --prefix="$PREFIX"
make -j"$(nproc)"
make install
