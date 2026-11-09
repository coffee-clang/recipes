#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "tiff-$VERSION"
./configure --prefix="$PREFIX" --disable-docs --enable-zlib --enable-zstd \
    --enable-lzma --disable-libdeflate --disable-jbig --disable-lerc \
    --disable-webp
make -j"$(nproc)"
make install
