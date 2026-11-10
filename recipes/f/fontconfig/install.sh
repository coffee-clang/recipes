#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "fontconfig-$VERSION"
# nofallback: upstream's wraps would otherwise fetch gperf from an unpinned
# git branch, and freetype or expat in place of the registry's copies.
meson setup build --prefix="$PREFIX" --libdir=lib --buildtype=release \
    --wrap-mode=nofallback \
    -Ddoc=disabled -Dtests=disabled -Dnls=disabled -Dcache-build=disabled \
    -Dxml-backend=expat -Diconv=disabled -Dfontations=disabled
meson compile -C build
meson install -C build
