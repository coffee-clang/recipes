#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "pcre-$VERSION"
./configure --prefix="$PREFIX"
make -j"$(nproc)"
make install
