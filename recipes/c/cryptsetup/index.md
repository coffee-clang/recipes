Title: cryptsetup
Date: 2026-02-12

# cryptsetup

## Version
2.7.5

## Description
cryptsetup is a library for setting up encrypted disk volumes using LUKS (Linux Unified Key Setup). It provides high-level API for block device encryption and is the foundation for Linux full-disk encryption.

## Dependencies
- libgcrypt
- libpopt
- popt
- json-c

## Recipe
#!/bin/bash
# Install script for cryptsetup
# Version: 2.7.5

set -e

VERSION="2.7.5"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://gitlab.com/cryptsetup/cryptsetup/-/archive/v${VERSION}/cryptsetup-v${VERSION}.tar.gz
tar xzf cryptsetup-v${VERSION}.tar.gz
cd cryptsetup-v${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --disable-cryptsetup-reencrypt
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/cryptsetup-v${VERSION}
