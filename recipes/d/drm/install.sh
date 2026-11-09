#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xJf "$ARCHIVE" --no-same-owner
cd "libdrm-$VERSION"
meson setup build --wrap-mode=nofallback --prefix="$PREFIX" --libdir=lib --buildtype=release -Dtests=false -Dman-pages=disabled -Dvalgrind=disabled -Dcairo-tests=disabled
meson compile -C build -j"$(nproc)"
meson install -C build
