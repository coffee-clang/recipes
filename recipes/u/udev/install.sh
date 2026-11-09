#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "systemd-$VERSION"
# Only libudev is wanted: configure systemd with optional features off, build
# the one library target and install it by hand. "meson install" would install
# all of systemd, including files under /etc and /usr/lib/systemd.
meson setup build --wrap-mode=nofallback --prefix="$PREFIX" --libdir=lib --buildtype=release \
    -Dmode=release -Dtests=false -Dman=disabled -Dhtml=disabled \
    -Dtranslations=false -Dselinux=disabled -Dapparmor=disabled \
    -Dlibcryptsetup=disabled -Dpam=disabled -Dacl=disabled -Daudit=disabled \
    -Dseccomp=disabled -Dblkid=disabled -Dkmod=disabled -Didn=false \
    -Dlibidn2=disabled -Dpcre2=disabled -Dglib=disabled -Ddbus=disabled \
    -Dbpf-framework=disabled -Dbootloader=disabled -Dukify=disabled
meson compile -C build udev:shared_library
mkdir -p "$PREFIX/include" "$PREFIX/lib/pkgconfig"
cp src/libudev/libudev.h "$PREFIX/include/"
cp -P build/libudev.so* "$PREFIX/lib/"
cp build/src/libudev/libudev.pc "$PREFIX/lib/pkgconfig/"
