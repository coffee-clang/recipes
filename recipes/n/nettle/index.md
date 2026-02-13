Title: nettle
Date: 2026-02-12

# nettle

## Version
3.10

## Description
Nettle is a low-level cryptographic library providing implementations of symmetric and asymmetric encryption algorithms. It is designed to be portable and is used by GnuTLS and other security applications.

## Dependencies
- gmp

## Recipe
#!/bin/bash
# Install script for nettle
# Version: 3.10

set -e

VERSION="3.10"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://ftp.gnu.org/gnu/nettle/nettle-${VERSION}.tar.gz
tar xzf nettle-${VERSION}.tar.gz
cd nettle-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/nettle-${VERSION}
