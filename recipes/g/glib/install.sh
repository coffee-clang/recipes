#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "glib-$VERSION"
meson setup build --wrap-mode=nofallback --prefix="$PREFIX" --libdir=lib --buildtype=release \
    -Dintrospection=disabled -Ddocumentation=false -Dman-pages=disabled \
    -Dtests=false -Dselinux=disabled -Dlibmount=disabled -Dsysprof=disabled
meson compile -C build
meson install -C build
