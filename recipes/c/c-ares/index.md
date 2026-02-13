Title: c-ares
Date: 2026-02-12

# c-ares

## Version
1.34.4

## Description
c-ares is a C library for asynchronous DNS requests and name resolution. It provides non-blocking DNS lookups and is used by curl, Apache Mesos, and many other projects requiring asynchronous name resolution.

## Dependencies
- cmake (build)

## License
MIT

## Recipe
#!/bin/bash
# Install script for c-ares
# Version: 1.34.4

set -e

VERSION="1.34.4"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://c-ares.org/download/c-ares-${VERSION}.tar.gz
tar xzf c-ares-${VERSION}.tar.gz
cd c-ares-${VERSION}

cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PREFIX"
cmake --build build -j$(nproc)
sudo cmake --install build
sudo ldconfig

rm -rf /tmp/c-ares-${VERSION}
