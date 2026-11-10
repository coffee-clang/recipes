#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "cairo-$VERSION"
# LZO is probed with no option to turn it off, and the registry has no recipe.
sed -i "s/dependency('lzo2', required: false)/dependency('', required: false)/" meson.build
meson setup build --prefix="$PREFIX" --libdir=lib --buildtype=release --wrap-mode=nodownload \
    -Dtests=disabled -Dgtk_doc=false -Dpng=enabled -Dfreetype=enabled \
    -Dfontconfig=enabled -Dzlib=enabled -Dglib=enabled -Dxlib=enabled -Dxcb=enabled \
    -Dxlib-xcb=disabled -Dspectre=disabled -Dsymbol-lookup=disabled
meson compile -C build
meson install -C build
