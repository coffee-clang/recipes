#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "libpciaccess-$VERSION"
meson setup build --wrap-mode=nodownload --prefix="$PREFIX" --libdir=lib --buildtype=release
meson compile -C build -j"$(nproc)"
meson install -C build
