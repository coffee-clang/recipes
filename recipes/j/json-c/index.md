Title: json-c
Date: 2026-02-12

# json-c

## Version
0.18

## Description
json-c provides a C library for parsing and manipulating JSON data. It supports JSON parsing, building, modification, and serialization with a simple object model and streaming API.

## Dependencies
- cmake

## Recipe
#!/bin/bash
# Install script for json-c
# Version: 0.18

set -e

VERSION="0.18"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://s3.amazonaws.com/json-c_releases/releases/json-c-${VERSION}.tar.gz
tar xzf json-c-${VERSION}.tar.gz
cd json-c-${VERSION}

cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PREFIX"
cmake --build build -j$(nproc)
sudo cmake --install build
sudo ldconfig

rm -rf /tmp/json-c-${VERSION}
