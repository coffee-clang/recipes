#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "libpsl-$VERSION"
./configure --prefix="$PREFIX" --enable-runtime=libidn2 \
    --enable-builtin --disable-man --disable-gtk-doc
make -j"$(nproc)"
make install
