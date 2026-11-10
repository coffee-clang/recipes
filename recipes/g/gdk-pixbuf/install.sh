#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "gdk-pixbuf-$VERSION"
meson setup build --prefix="$PREFIX" --libdir=lib --buildtype=release --wrap-mode=nodownload \
    -Dpng=enabled -Djpeg=enabled -Dtiff=enabled -Dgif=enabled -Dothers=disabled \
    -Dintrospection=disabled -Dman=false -Dgtk_doc=false -Ddocs=false \
    -Dtests=false -Dinstalled_tests=false
meson compile -C build
meson install -C build
