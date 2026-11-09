#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "vte-$VERSION"
meson setup build --prefix="$PREFIX" --libdir=lib --buildtype=release --wrap-mode=nofallback \
    -Dgtk3=true -Dgtk4=false -Dgir=false -Dvapi=false -Ddocs=false \
    -Dgnutls=false -Dicu=false -D_systemd=false
meson compile -C build
meson install -C build
