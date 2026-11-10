#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "ffmpeg-$VERSION"
# libx264 is GPL, so the build must be GPL too.
./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --enable-shared --enable-gpl --enable-libx264 --disable-doc
make -j"$(nproc)"
make install
