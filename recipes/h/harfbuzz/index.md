Title: harfbuzz
Date: 2026-02-12

# harfbuzz

## Version
10.0.1

## Description
HarfBuzz is a text shaping library for OpenType and Graphite fonts. It determines how to render Unicode text and is used by GNOME, Firefox, LibreOffice, and other applications for proper text rendering.

## Dependencies
- glib
- freetype
- cairo
- icu (optional)

## Recipe
#!/bin/bash
# Install script for HarfBuzz
# Version: 10.0.1

set -e

VERSION="10.0.1"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/harfbuzz/harfbuzz/releases/download/${VERSION}/harfbuzz-${VERSION}.tar.xz
tar xf harfbuzz-${VERSION}.tar.xz
cd harfbuzz-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --with-glib
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/harfbuzz-${VERSION}
