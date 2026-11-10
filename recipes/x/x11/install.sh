#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "libX11-$VERSION"
./configure --prefix="$PREFIX" --disable-specs
make -j"$(nproc)"
make install
