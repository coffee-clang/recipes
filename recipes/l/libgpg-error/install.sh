#!/bin/bash
set -e -o pipefail -u

tar xjf "$ARCHIVE" --no-same-owner
cd "libgpg-error-$VERSION"
./configure --prefix="$PREFIX" --disable-doc
make -j"$(nproc)"
make install
