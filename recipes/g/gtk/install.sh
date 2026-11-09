#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xJf "$ARCHIVE" --no-same-owner
cd "gtk-$VERSION"
# X11 only: the Wayland backend requires xkbcommon, which cannot be built here.
# The cups print backend and colord would link host libraries with no recipe.
meson setup build --prefix="$PREFIX" --libdir=lib --buildtype=release --wrap-mode=nofallback \
    -Dx11_backend=true -Dwayland_backend=false -Dbroadway_backend=false \
    -Dxinerama=yes -Dprint_backends=file,lpr -Dcolord=no -Dcloudproviders=false \
    -Dtracker3=false -Dprofiler=false \
    -Dintrospection=false -Ddemos=false -Dexamples=false -Dtests=false \
    -Dinstalled_tests=false -Dgtk_doc=false -Dman=false
meson compile -C build
meson install -C build
