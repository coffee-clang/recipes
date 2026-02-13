Title: jansson
Date: 2026-02-12

# jansson

## Version
2.14

## Description
Jansson is a C library for encoding, decoding, and manipulating JSON data. It provides a simple API and is known for its small size, ease of use, and good performance.

## Dependencies
- cmake (build)

## License
MIT

## Recipe
#!/bin/bash
# Install script for jansson
# Version: 2.14

set -e

VERSION="2.14"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/akheron/jansson/releases/download/v${VERSION}/jansson-${VERSION}.tar.gz
tar xzf jansson-${VERSION}.tar.gz
cd jansson-${VERSION}

cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PREFIX"
cmake --build build -j$(nproc)
sudo cmake --install build
sudo ldconfig

rm -rf /tmp/jansson-${VERSION}
