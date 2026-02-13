Title: freetype
Date: 2026-02-12

# freetype

## Version
2.13.3

## Description
FreeType is a freely available software library for rendering fonts. It provides a uniform interface to access font content and is used by most Linux desktop environments, browsers, and ebook readers.

## Dependencies
- zlib (optional, for bitmap fonts)

## License
FreeType
- brotli (optional, for color emoji)

## Recipe
#!/bin/bash
# Install script for FreeType
# Version: 2.13.3

set -e

VERSION="2.13.3"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://download.savannah.nongnu.org/releases/freetype/freetype-${VERSION}.tar.gz
tar xzf freetype-${VERSION}.tar.gz
cd freetype-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/freetype-${VERSION}
