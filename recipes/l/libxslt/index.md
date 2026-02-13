Title: libxslt
Date: 2026-02-12

# libxslt

## Version
1.1.42

## Description
libxslt is the XSLT C library for XML transformation. It implements XSLT version 1.0 and EXSLT extensions, providing stylesheet processing for converting XML documents to other formats.

## Dependencies
- libxml2

## License
MIT

## Recipe
#!/bin/bash
# Install script for libxslt
# Version: 1.1.42

set -e

VERSION="1.1.42"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://download.gnome.org/sources/libxslt/${VERSION%.*}/libxslt-${VERSION}.tar.gz
tar xzf libxslt-${VERSION}.tar.gz
cd libxslt-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --without-python --without-crypto
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/libxslt-${VERSION}
