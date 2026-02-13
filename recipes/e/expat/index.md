Title: expat
Date: 2026-02-12

# expat

## Version
2.6.4

## Description
Expat is a stream-oriented XML parser library written in C. It is widely used for parsing XML documents, particularly in projects like Firefox, Apache HTTP Server, and Python's xml.etree module.

## Dependencies
- None (pure C library)

## License
MIT

## Recipe
#!/bin/bash
# Install script for expat
# Version: 2.6.4

set -e

VERSION="2.6.4"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/libexpat/libexpat/releases/download/R_${VERSION//./_}/expat-${VERSION}.tar.gz
tar xzf expat-${VERSION}.tar.gz
cd expat-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --without-docbook
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/expat-${VERSION}
