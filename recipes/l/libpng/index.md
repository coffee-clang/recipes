Title: libpng
Date: 2026-02-12

# libpng

## Version
1.6.46

## Description
libpng is the official PNG reference library for reading and writing PNG (Portable Network Graphics) images. It provides comprehensive PNG functionality including compression, filtering, and progressive image loading.

## Dependencies
- zlib

## Recipe
#!/bin/bash
# Install script for libpng
# Version: 1.6.46

set -e

VERSION="1.6.46"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://sourceforge.net/projects/libpng/files/libpng${VERSION}/libpng-${VERSION}.tar.gz
tar xzf libpng-${VERSION}.tar.gz
cd libpng-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/libpng-${VERSION}
