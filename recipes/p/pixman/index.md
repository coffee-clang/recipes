Title: pixman
Date: 2026-02-12

# pixman

## Version
0.44.2

## Description
Pixman is a low-level software pixel manipulation library providing image compositing and rectangle filling functions. It is used by Cairo, Mozilla Firefox, and other applications for fast software rendering.

## Dependencies
- meson or autoconf

## License
MIT

## Recipe
#!/bin/bash
# Install script for pixman
# Version: 0.44.2

set -e

VERSION="0.44.2"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://cairographics.org/releases/pixman-${VERSION}.tar.gz
tar xzf pixman-${VERSION}.tar.gz
cd pixman-${VERSION}

meson setup build --prefix="$PREFIX" -Dtests=false
meson compile -C build
sudo meson install -C build

rm -rf /tmp/pixman-${VERSION}
