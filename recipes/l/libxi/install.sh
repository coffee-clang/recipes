#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "libXi-$VERSION"
./configure --prefix="$PREFIX" --disable-docs --disable-specs --without-xmlto --without-fop --without-asciidoc
make -j"$(nproc)"
make install
