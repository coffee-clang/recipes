Title: bzip2
Date: 2026-02-12

# bzip2

## Version
1.0.8

## Description
bzip2 is a free, open-source lossless compression library known for its high compression ratio. It uses the Burrows-Wheeler transform and provides better compression than gzip but at slower speeds.

## Dependencies
- None (pure C library)

## License
bzip2

## Recipe
#!/bin/bash
# Install script for bzip2
# Version: 1.0.8

set -e

VERSION="1.0.8"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://sourceware.org/pub/bzip2/bzip2-${VERSION}.tar.gz
tar xzf bzip2-${VERSION}.tar.gz
cd bzip2-${VERSION}

make -j$(nproc) CFLAGS="-fPIC -O2"
sudo make install PREFIX="$PREFIX"
sudo ldconfig

rm -rf /tmp/bzip2-${VERSION}
