Title: speex
Date: 2026-02-12

# speex

## Version
1.2.1

## Description
Speex is a patent-free audio codec optimized for voice compression. It provides excellent quality for voice at low bitrates and was widely used for VoIP applications before Opus became the standard.

## Dependencies
- libogg

## License
BSD-3-Clause
- autoconf/automake

## Recipe
#!/bin/bash
# Install script for Speex
# Version: 1.2.1

set -e

VERSION="1.2.1"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://downloads.xiph.org/releases/speex/speex-${VERSION}.tar.gz
tar xzf speex-${VERSION}.tar.gz
cd speex-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/speex-${VERSION}
