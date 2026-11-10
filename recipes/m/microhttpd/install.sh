#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "libmicrohttpd-$VERSION"
./configure --prefix="$PREFIX" --disable-doc --disable-examples
make -j"$(nproc)"
make install
