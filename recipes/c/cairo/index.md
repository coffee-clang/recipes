Title: cairo
Date: 2026-02-12

# cairo

## Version
1.18.2

## Description
Cairo is a 2D graphics library supporting multiple output targets including X Window System, Quartz, Win32, image buffers, and PDF. It provides vector graphics primitives and is the rendering engine for GTK+ and many other applications.

## Dependencies
- libpng

## License
LGPL-2.1
- freetype
- fontconfig
- pixman

## Recipe
#!/bin/bash
# Install script for cairo
# Version: 1.18.2

set -e

VERSION="1.18.2"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://www.cairographics.org/releases/cairo-${VERSION}.tar.xz
tar xf cairo-${VERSION}.tar.xz
cd cairo-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --disable-xlib
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/cairo-${VERSION}
