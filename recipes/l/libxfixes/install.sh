#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "libXfixes-$VERSION"
./configure --prefix="$PREFIX"
make -j"$(nproc)"
make install
