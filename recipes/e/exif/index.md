Title: exif
Date: 2026-02-12

# libexif

## Version
0.6.24

## Description
libexif is a library for parsing, editing, and saving EXIF metadata from digital camera images. It supports reading and writing EXIF tags from JPEG, TIFF, and PNG files.

## Dependencies
- libjpeg
- pkg-config

## Recipe
#!/bin/bash
# Install script for libexif
# Version: 0.6.24

set -e

VERSION="0.6.24"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/libexif/libexif/releases/download/v${VERSION}/libexif-${VERSION}.tar.gz
tar xzf libexif-${VERSION}.tar.gz
cd libexif-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/libexif-${VERSION}
