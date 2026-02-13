Title: libassuan
Date: 2026-02-12

# libassuan

## Version
2.5.8

## Description
Libassuan is a library implementing the Assuan protocol used by GnuPG for inter-process communication. It provides a generic IPC mechanism for applications requiring secure communication.

## Dependencies
- libgpg-error

## License
LGPL-2.1

## Recipe
#!/bin/bash
# Install script for libassuan
# Version: 2.5.8

set -e

VERSION="2.5.8"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://gnupg.org/ftp/gcrypt/libassuan/libassuan-${VERSION}.tar.bz2
tar xjf libassuan-${VERSION}.tar.bz2
cd libassuan-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/libassuan-${VERSION}
