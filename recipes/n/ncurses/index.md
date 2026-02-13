Title: ncurses
Date: 2026-02-12

# ncurses

## Version
6.5

## Description
ncurses is a programming library providing an API for building terminal user interfaces. It extends the basic terminal capabilities allowing colored text, forms, menus, and windows. Used by most terminal applications.

## Dependencies
- None (self-contained)

## License
MIT

## Recipe
#!/bin/bash
# Install script for ncurses
# Version: 6.5

set -e

VERSION="6.5"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://ftp.gnu.org/gnu/ncurses/ncurses-${VERSION}.tar.gz
tar xzf ncurses-${VERSION}.tar.gz
cd ncurses-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --without-ada --without-cxx-binding
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/ncurses-${VERSION}
