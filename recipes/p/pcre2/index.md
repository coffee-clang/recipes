Title: pcre2
Date: 2026-02-12

# pcre2

## Version
10.44

## Description
PCRE2 is the successor to PCRE, implementing regular expressions with improved features including better Unicode support, multiple matching modes, and improved performance. It is the modern replacement for PCRE.

## Dependencies
- cmake (build)

## License
BSD

## Recipe
#!/bin/bash
# Install script for PCRE2
# Version: 10.44

set -e

VERSION="10.44"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/PCRE2Project/pcre2/releases/download/pcre2-${VERSION}/pcre2-${VERSION}.tar.gz
tar xzf pcre2-${VERSION}.tar.gz
cd pcre2-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --enable-utf8 --enable-unicode-properties
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/pcre2-${VERSION}
