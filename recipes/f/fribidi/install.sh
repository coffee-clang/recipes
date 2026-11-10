#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "fribidi-$VERSION"
meson setup build --wrap-mode=nodownload --prefix="$PREFIX" --libdir=lib --buildtype=release \
    -Ddocs=false -Dtests=false -Dbin=false
meson compile -C build
meson install -C build
