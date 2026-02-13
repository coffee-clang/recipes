Title: x11
Date: 2026-02-12

# x11

## Version
1.8.9

## Description
X11 (X Window System) is the foundation for graphical user interfaces on Unix-like systems. libX11 provides the client library for connecting to X servers and creating graphical applications.

## Dependencies
- xorgproto

## License
MIT
- libxcb (optional)

## Recipe
#!/bin/bash
# Install script for libX11
# Version: 1.8.9

set -e

VERSION="1.8.9"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://x.org/archive/individual/lib/libX11-${VERSION}.tar.xz
tar xf libX11-${VERSION}.tar.xz
cd libX11-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/libX11-${VERSION}
