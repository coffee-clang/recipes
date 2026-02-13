Title: opus
Date: 2026-02-12

# opus

## Version
1.5.2

## Description
Opus is a lossy audio codec designed for interactive speech and music transmission over the internet. It provides excellent quality at low bitrates and is used by VoIP applications, streaming, and video conferencing.

## Dependencies
- cmake

## Recipe
#!/bin/bash
# Install script for opus
# Version: 1.5.2

set -e

VERSION="1.5.2"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://archive.mozilla.org/pub/opus/opus-${VERSION}.tar.gz
tar xzf opus-${VERSION}.tar.gz
cd opus-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/opus-${VERSION}
