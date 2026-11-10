#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "libdatrie-$VERSION"
./configure --prefix="$PREFIX" --disable-doxygen-doc
make -j"$(nproc)"
make install
