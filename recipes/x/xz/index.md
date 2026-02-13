Title: xz
Date: 2026-02-12

# xz

## Version
5.6.3

## Description
XZ Utils is a set of tools for the .xz compression format. liblzma provides the LZMA compression algorithm implementation, offering high compression ratios for data storage and distribution.

## Dependencies
- None (self-contained)

## Recipe
#!/bin/bash
# Install script for XZ Utils
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
