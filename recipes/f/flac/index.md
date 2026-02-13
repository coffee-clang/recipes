Title: flac
Date: 2026-02-12

# flac

## Version
1.4.3

## Description
FLAC (Free Lossless Audio Codec) is an audio coding format for lossless compression of digital audio. The libFLAC library provides the reference encoder and decoder, supporting FLAC levels 0-8.

## Dependencies
- libogg

## License
BSD-3-Clause
- cmake

## Recipe
#!/bin/bash
# Install script for FLAC
# Version: 1.4.3

set -e

VERSION="1.4.3"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://downloads.xiph.org/flac/flac-${VERSION}.tar.xz
tar xf flac-${VERSION}.tar.xz
cd flac-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/flac-${VERSION}
