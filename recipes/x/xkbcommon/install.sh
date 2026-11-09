#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "libxkbcommon-xkbcommon-$VERSION"
meson setup build --wrap-mode=nofallback --prefix="$PREFIX" --libdir=lib --buildtype=release -Denable-docs=false -Denable-tools=false -Denable-wayland=false -Denable-x11=true -Denable-xkbregistry=false
meson compile -C build -j"$(nproc)"
meson install -C build
