Title: brotli
Date: 2026-02-12

# brotli

## Version
1.1.0

## Description
Brotli is a lossless compression algorithm developed by Google. It provides better compression ratios than gzip while maintaining similar speed, widely used for web content compression (Content-Encoding: br).

## Dependencies
- cmake

## License
BSD-3-Clause

## Recipe
#!/bin/bash
# Install script for brotli
# Version: 1.1.0

set -e

VERSION="1.1.0"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
git clone --depth 1 --branch v${VERSION} https://github.com/google/brotli.git
cd brotli

cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PREFIX"
cmake --build build -j$(nproc)
sudo cmake --install build
sudo ldconfig

rm -rf /tmp/brotli
