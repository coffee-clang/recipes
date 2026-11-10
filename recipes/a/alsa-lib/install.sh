#!/bin/bash
set -e -o pipefail -u

tar xjf "$ARCHIVE" --no-same-owner
cd "alsa-lib-$VERSION"
./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j"$(nproc)"
make install
