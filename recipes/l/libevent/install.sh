#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "libevent-$VERSION-stable"
./configure --prefix="$PREFIX"
make -j"$(nproc)"
make install
