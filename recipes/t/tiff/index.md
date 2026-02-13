Title: tiff
Date: 2026-02-12

# tiff

## Version
4.7.0

## Description
LibTIFF provides support for the Tag Image File Format (TIFF), a widely used format for high-quality image storage. It provides functions for reading, writing, and manipulating TIFF images.

## Dependencies
- libjpeg

## License
MIT
- zlib

## Recipe
#!/bin/bash
# Install script for libtiff
# Version: 4.7.0

set -e

VERSION="4.7.0"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://download.osgeo.org/libtiff/tiff-${VERSION}.tar.gz
tar xzf tiff-${VERSION}.tar.gz
cd tiff-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/tiff-${VERSION}
