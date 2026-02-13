Title: cjson
Date: 2026-02-12

# cjson

## Version
1.7.18

## Description
cJSON is an ultra-lightweight JSON parser and writer for C. It is designed to be minimal, fast, and easy to integrate into any C project. It is one of the most popular JSON libraries for C.

## Dependencies
- None (pure C library)

## Recipe
#!/bin/bash
# Install script for cJSON
# Version: 1.7.18

set -e

VERSION="1.7.18"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
git clone --depth 1 --branch ${VERSION} https://github.com/DaveGamble/cJSON.git
cd cJSON

cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PREFIX" -DENABLE_CJSON_TEST=OFF
cmake --build build -j$(nproc)
sudo cmake --install build
sudo ldconfig

rm -rf /tmp/cJSON
