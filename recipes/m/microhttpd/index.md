Title: microhttpd
Date: 2026-02-12

# microhttpd

## Version
1.0.0

## Description
GNU libmicrohttpd is a small, embeddable HTTP server library. It supports HTTP/1.1, HTTPS, chunked transfer encoding, and multiple threading models. It is designed for embedding HTTP server functionality into applications.

## Dependencies
- libgnutls (optional)

## Recipe
#!/bin/bash
# Install script for libmicrohttpd
# Version: 1.0.0

set -e

VERSION="1.0.0"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-${VERSION}.tar.gz
tar xzf libmicrohttpd-${VERSION}.tar.gz
cd libmicrohttpd-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/libmicrohttpd-${VERSION}
