Title: libxml2
Date: 2026-02-12

# libxml2

## Version
2.12.9

## Description
libxml2 is the XML C parser and toolkit developed for the GNOME project. It provides interfaces for parsing and manipulating XML documents, supporting XPath, XPointer, XInclude, and HTML parsing.

## Dependencies
- python3 (optional)

## License
MIT
- zlib (optional)

## Recipe
#!/bin/bash
# Install script for libxml2
# Version: 2.12.9

set -e

VERSION="2.12.9"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://download.gnome.org/sources/libxml2/${VERSION%.*}/libxml2-${VERSION}.tar.gz
tar xzf libxml2-${VERSION}.tar.gz
cd libxml2-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --without-python
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/libxml2-${VERSION}
