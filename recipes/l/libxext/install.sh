#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "libXext-$VERSION"
./configure --prefix="$PREFIX" --disable-specs --without-xmlto --without-fop --without-xsltproc
make -j"$(nproc)"
make install
