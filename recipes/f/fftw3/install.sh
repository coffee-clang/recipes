#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "fftw-$VERSION"
./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --enable-shared
make -j"$(nproc)"
make install
