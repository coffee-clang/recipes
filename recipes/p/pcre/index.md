Title: pcre
Date: 2026-02-12

# pcre

## Version
8.45

## Description
PCRE (Perl Compatible Regular Expressions) is a library implementing regular expression pattern matching. It provides functionality similar to Perl's regex engine and is used by many applications including grep, Apache, and PHP.

## Dependencies
- None (self-contained)

## Recipe
#!/bin/bash
# Install script for PCRE
# Version: 8.45

set -e

VERSION="8.45"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://sourceforge.net/projects/pcre/files/pcre/${VERSION}/pcre-${VERSION}.tar.gz
tar xzf pcre-${VERSION}.tar.gz
cd pcre-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --enable-utf8 --enable-unicode-properties
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/pcre-${VERSION}
