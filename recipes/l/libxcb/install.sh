#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "libxcb-$VERSION"
./configure --prefix="$PREFIX" --without-doxygen
make -j"$(nproc)"
make install
