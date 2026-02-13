Title: attr
Date: 2026-02-12

# attr

## Version
2.5.2

## Description
The attr library provides extended attributes support for filesystems on Linux. Extended attributes allow storing additional metadata (key-value pairs) associated with files, used by SELinux, ACLs, and other filesystem features.

## Dependencies
- gettext (for internationalization)

## License
LGPL-2.1

## Recipe
#!/bin/bash
# Install script for attr
# Version: 2.5.2

set -e

VERSION="2.5.2"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://download.savannah.nongnu.org/releases/attr/attr-${VERSION}.tar.gz
tar xzf attr-${VERSION}.tar.gz
cd attr-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/attr-${VERSION} /tmp/attr-${VERSION}.tar.gz
