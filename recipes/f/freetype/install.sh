#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "freetype-$VERSION"
# HarfBuzz depends on FreeType, so linking it back would be circular. The other
# optional codecs are left out so only the declared zlib is used.
./configure --prefix="$PREFIX" --with-zlib=yes --with-harfbuzz=no \
    --with-png=no --with-bzip2=no --with-brotli=no
make -j"$(nproc)"
make install
