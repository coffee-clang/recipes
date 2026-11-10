#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
# Since 2.46 ATK ships inside at-spi2-core, together with the atk-bridge that
# GTK links against. Building the whole module keeps the two in step.
cd "at-spi2-core-$VERSION"
meson setup build --wrap-mode=nofallback --prefix="$PREFIX" --libdir=lib --buildtype=release \
    -Dintrospection=disabled -Ddocs=false -Dx11=disabled
meson compile -C build
meson install -C build
