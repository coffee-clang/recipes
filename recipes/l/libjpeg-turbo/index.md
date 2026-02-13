Title: libjpeg-turbo
Date: 2026-02-12

# libjpeg-turbo

## Version
3.0.4

## Description
libjpeg-turbo is a JPEG image codec that uses SIMD instructions to accelerate baseline JPEG compression and decompression. It provides significantly faster performance than libjpeg while maintaining compatibility.

## Dependencies
- cmake (build)

## License
BSD-3-Clause

## Recipe
#!/bin/bash
# Install script for libjpeg-turbo
# Version: 3.0.4

set -e

VERSION="3.0.4"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://sourceforge.net/projects/libjpeg-turbo/files/${VERSION}/libjpeg-turbo-${VERSION}.tar.gz
tar xzf libjpeg-turbo-${VERSION}.tar.gz
cd libjpeg-turbo-${VERSION}

cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PREFIX"
cmake --build build -j$(nproc)
sudo cmake --install build
sudo ldconfig

rm -rf /tmp/libjpeg-turbo-${VERSION}
