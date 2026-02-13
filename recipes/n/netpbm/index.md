Title: netpbm
Date: 2026-02-12

# netpbm

## Version
11.0.0

## Description
Netpbm is a toolkit for manipulation of graphic images including conversion between over 100 formats. It provides utilities for image conversion, editing, and analysis used by many graphics applications.

## Dependencies
- libjpeg

## License
BSD-3-Clause
- libpng
- libtiff

## Recipe
#!/bin/bash
# Install script for Netpbm
# Version: 11.0.0

set -e

VERSION="11.0.0"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://sourceforge.net/projects/netpbm/advanced/11.0.0/netpbm-${VERSION}.tgz
tar xzf netpbm-${VERSION}.tgz
cd netpbm-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --with-jpeg=/usr --with-tiff=/usr --with-png=/usr
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/netpbm-${VERSION}
