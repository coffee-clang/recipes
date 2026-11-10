#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "LVM2.$VERSION"
# Only libdevmapper is built; udev, systemd, selinux and blkid are off.
./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" \
    --with-usrlibdir="$PREFIX/lib" --enable-pkgconfig --disable-nls \
    --disable-selinux --without-udev --disable-udev_sync --without-systemd \
    --disable-sd-notify --disable-systemd-journal --disable-app-machineid \
    --without-blkid --disable-blkid_wiping --without-libaio --disable-readline
make -j"$(nproc)" libdm
make -C libdm install install_pkgconfig
