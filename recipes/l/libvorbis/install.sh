#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "libvorbis-$VERSION"
./configure --prefix="$PREFIX" --disable-docs --disable-examples \
    --disable-oggtest
make -j"$(nproc)"
make install
