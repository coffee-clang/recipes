Title: wavpack
Date: 2026-02-12

# wavpack

## Version
5.7.0

## Description
WavPack is a free, open-source audio codec providing both lossless and lossy compression. It offers excellent quality and is used by audio production software and music collection management.

## Dependencies
- cmake

## Recipe
#!/bin/bash
# Install script for WavPack
# Version: 5.7.0

set -e

VERSION="5.7.0"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
git clone --depth 1 --branch ${VERSION} https://github.com/dbry/WavPack.git
cd WavPack

cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PREFIX"
cmake --build build -j$(nproc)
sudo cmake --install build
sudo ldconfig

rm -rf /tmp/WavPack
