#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "popt-$VERSION"
./configure --prefix="$PREFIX" --disable-nls
make -j"$(nproc)"
make install
