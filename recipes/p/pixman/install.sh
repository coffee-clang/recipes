#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "pixman-$VERSION"
meson setup build --wrap-mode=nodownload --prefix="$PREFIX" --libdir=lib --buildtype=release \
    -Dtests=disabled -Ddemos=disabled -Dgtk=disabled -Dlibpng=disabled
meson compile -C build
meson install -C build
