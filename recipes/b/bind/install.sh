#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "bind-$VERSION"
./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --disable-doh \
    --enable-linux-caps --with-json-c --with-libxml2 --with-lmdb --with-zlib \
    --with-readline=readline --with-gssapi=no --without-libidn2 \
    --without-jemalloc --disable-geoip --without-cmocka
make -j"$(nproc)"
make install
