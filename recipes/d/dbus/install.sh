#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "dbus-$VERSION"
meson setup build --wrap-mode=nofallback --prefix="$PREFIX" --libdir=lib --buildtype=release \
    -Ddoxygen_docs=disabled -Dxml_docs=disabled -Dducktype_docs=disabled \
    -Dqt_help=disabled -Dmodular_tests=disabled -Dsystemd=disabled \
    -Dselinux=disabled -Dapparmor=disabled -Dlibaudit=disabled -Dx11_autolaunch=disabled
meson compile -C build
meson install -C build
