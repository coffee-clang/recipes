#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "harfbuzz-$VERSION"
meson setup build --prefix="$PREFIX" --libdir=lib --buildtype=release --wrap-mode=nofallback \
    -Dtests=disabled -Ddocs=disabled -Dintrospection=disabled -Dutilities=disabled \
    -Dglib=enabled -Dgobject=enabled -Dfreetype=enabled -Dcairo=disabled -Dicu=disabled \
    -Dchafa=disabled -Dgraphite2=disabled
meson compile -C build
meson install -C build
