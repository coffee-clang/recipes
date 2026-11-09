#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
# The archive is named after a commit, and so is its top directory.
cd "${ARCHIVE%.tar.gz}"
# Shared and PIC: consumers such as FFmpeg link against a shared libx264.
./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --enable-shared --enable-pic
make -j"$(nproc)"
make install
