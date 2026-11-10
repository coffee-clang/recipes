#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "libXcursor-$VERSION"
./configure --prefix="$PREFIX"
make -j"$(nproc)"
make install
