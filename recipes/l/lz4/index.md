Title: lz4
Date: 2026-02-12

# lz4

## Version
1.10.0

## Description
LZ4 is a lossless compression algorithm focusing on speed. It provides extremely fast compression and decompression, making it ideal for scenarios where speed is more important than maximum compression ratio.

## Dependencies
- cmake

## Recipe
#!/bin/bash
# Install script for LZ4
# Version: 1.10.0

set -e

VERSION="1.10.0"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
git clone --depth 1 --branch v${VERSION} https://github.com/lz4/lz4.git
cd lz4

make -j$(nproc) BUILD_STATIC=1
sudo make install PREFIX="$PREFIX"
sudo ldconfig

rm -rf /tmp/lz4
