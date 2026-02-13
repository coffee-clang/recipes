Title: zstd
Date: 2026-02-12

# zstd

## Version
1.5.6

## Description
Zstandard (zstd) is a real-time compression algorithm developed by Facebook. It provides excellent compression ratios with very fast speeds, making it suitable for data compression, backups, and content distribution.

## Dependencies
- cmake

## Recipe
#!/bin/bash
# Install script for Zstandard
# Version: 1.5.6

set -e

VERSION="1.5.6"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
git clone --depth 1 --branch v${VERSION} https://github.com/facebook/zstd.git
cd zstd

make -j$(nproc) DESTDIR="$PREFIX" install
sudo ldconfig

rm -rf /tmp/zstd
