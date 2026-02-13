Title: qrencode
Date: 2026-02-12

# qrencode

## Version
4.1.1

## Description
QRencode is a fast QR code encoder library. It converts strings or URLs into QR code images that can be scanned by mobile phones and barcode readers.

## Dependencies
- libpng (optional)

## License
LGPL-2.1

## Recipe
#!/bin/bash
# Install script for qrencode
# Version: 4.1.1

set -e

VERSION="4.1.1"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/fukuchi/libqrencode/archive/refs/tags/v${VERSION}.tar.gz
tar xzf v${VERSION}.tar.gz
cd libqrencode-${VERSION}

./autogen.sh --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/libqrencode-${VERSION}
