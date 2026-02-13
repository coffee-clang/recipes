Title: util-linux
Date: 2026-02-12

# util-linux

## Version
2.40.2

## Description
util-linux is a collection of essential Linux system utilities including mount, umount, fdisk, mkfs, and many other fundamental command-line tools. Many of these are essential for system administration.

## Dependencies
- ncurses

## License
GPL-2.0
- libcap-ng
- libsmartcols

## Recipe
#!/bin/bash
# Install script for util-linux
# Version: 2.40.2

set -e

VERSION="2.40.2"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/karelzak/util-linux/archive/refs/tags/v${VERSION}.tar.gz
tar xzf v${VERSION}.tar.gz
cd util-linux-${VERSION}

./autogen.sh --prefix="$PREFIX" --libdir="$PREFIX/lib" --disable-makeinstall-chown --disable-makeinstall-setuid
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/util-linux-${VERSION}
