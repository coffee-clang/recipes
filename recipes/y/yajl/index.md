Title: yajl
Date: 2026-02-12

# yajl

## Version
2.1.0

## Description
YAJL (Yet Another JSON Library) is a small, event-driven JSON parser and generator for C. It provides streaming parsing for large JSON documents and is used by many applications.

## Dependencies
- cmake

## Recipe
#!/bin/bash
# Install script for YAJL
# Version: 2.1.0

set -e

VERSION="2.1.0"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/lloyd/yajl/archive/refs/tags/${VERSION}.tar.gz
tar xzf ${VERSION}.tar.gz
cd yajl-${VERSION}

cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PREFIX"
cmake --build build -j$(nproc)
sudo cmake --install build
sudo ldconfig

rm -rf /tmp/yajl-${VERSION}
