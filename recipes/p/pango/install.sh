#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "pango-$VERSION"
meson setup build --prefix="$PREFIX" --libdir=lib --buildtype=release --wrap-mode=nofallback \
    -Dintrospection=disabled -Dbuild-testsuite=false -Dbuild-examples=false \
    -Dcairo=enabled -Dfreetype=enabled -Dfontconfig=enabled -Dxft=enabled \
    -Dlibthai=enabled -Dsysprof=disabled -Ddocumentation=false
meson compile -C build
meson install -C build
