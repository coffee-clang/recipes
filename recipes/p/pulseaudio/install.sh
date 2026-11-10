#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "pulseaudio-$VERSION"
meson setup build --wrap-mode=nofallback --prefix="$PREFIX" --libdir=lib --buildtype=release \
    -Ddaemon=false -Dclient=true -Dtests=false -Ddoxygen=false -Dman=false \
    -Dglib=enabled -Ddatabase=simple -Dbashcompletiondir=no -Dzshcompletiondir=no \
    -Ddbus=enabled -Dsystemd=disabled -Dx11=disabled
meson compile -C build
meson install -C build
