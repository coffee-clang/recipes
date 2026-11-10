#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "libxml2-$VERSION"
./configure --prefix="$PREFIX" --without-python
make -j"$(nproc)"
make install
