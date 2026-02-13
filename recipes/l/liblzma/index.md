Title: liblzma
Date: 2026-02-12

# liblzma

## Version
5.6.3

## Description
liblzma provides LZMA compression and decompression functionality. It is part of the XZ Utils package and implements the LZMA algorithm used in the .xz format, offering high compression ratios.

## Dependencies
- None (self-contained)

## Recipe
#!/bin/bash
# Install script for liblzma
# Version: 5.6.3

set -e

VERSION="5.6.3"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://tukaani.org/xz/xz-${VERSION}.tar.gz
tar xzf xz-${VERSION}.tar.gz
cd xz-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --disable-docs
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/xz-${VERSION}
