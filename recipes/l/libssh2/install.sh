#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "libssh2-$VERSION"
./configure --prefix="$PREFIX" --with-crypto=openssl --disable-examples-build \
    --with-libz
make -j"$(nproc)"
make install
