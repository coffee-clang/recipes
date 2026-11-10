#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "fontconfig-$VERSION"
# nodownload: upstream's wraps would otherwise fetch gperf from an unpinned
# git branch (nofallback does not stop program fallbacks).
meson setup build --prefix="$PREFIX" --libdir=lib --buildtype=release \
    --wrap-mode=nodownload \
    -Ddoc=disabled -Dtests=disabled -Dnls=disabled -Dcache-build=disabled \
    -Dxml-backend=expat -Diconv=disabled -Dfontations=disabled
meson compile -C build
meson install -C build
