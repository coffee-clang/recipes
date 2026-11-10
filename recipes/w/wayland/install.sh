#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "wayland-$VERSION"
meson setup build --wrap-mode=nodownload --prefix="$PREFIX" --libdir=lib --buildtype=release \
    -Ddocumentation=false -Dtests=false -Ddtd_validation=false
meson compile -C build
meson install -C build
