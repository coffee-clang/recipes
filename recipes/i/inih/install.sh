#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "inih-$VERSION"
meson setup build --wrap-mode=nofallback --prefix="$PREFIX" --libdir=lib --buildtype=release \
    -Ddefault_library=both -Ddistro_install=true
ninja -C build
ninja -C build install
