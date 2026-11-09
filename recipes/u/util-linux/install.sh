#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xJf "$ARCHIVE" --no-same-owner
cd "util-linux-$VERSION"
# Libraries only: the programs need root to install (setuid, chown, udev).
./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" \
    --disable-all-programs --enable-libuuid --enable-libblkid \
    --enable-libmount --enable-libsmartcols --enable-libfdisk \
    --disable-bash-completion --disable-makeinstall-chown \
    --disable-makeinstall-setuid --without-systemd --without-udev \
    --without-python --disable-nls
make -j"$(nproc)"
make install
