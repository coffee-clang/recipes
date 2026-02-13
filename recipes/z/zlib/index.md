Title: zlib
Date: 2026-02-12

# zlib

## Version
1.3.1

## Description
zlib is a massively portable, free, general-purpose, legally unencumbered lossless compression library. It implements the DEFLATE algorithm used by gzip, PNG, and many other formats. It is one of the most widely used C libraries.

## Dependencies
- None (self-contained)

## License
zlib

## Recipe
#!/bin/bash
# Install script for zlib
# Version: 1.3.1

set -e

VERSION="1.3.1"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/madler/zlib/archive/refs/tags/v${VERSION}.tar.gz
tar xzf v${VERSION}.tar.gz
cd zlib-${VERSION}

./configure --prefix="$PREFIX"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/zlib-${VERSION}
