Title: sqlite
Date: 2026-02-12

# sqlite

## Version
3.47.2

## Description
SQLite is a small, fast, self-contained, high-reliability, full-featured SQL database engine. It is the most widely used database engine in the world, embedded in countless applications from browsers to mobile phones.

## Dependencies
- None (self-contained)

## License
Public Domain

## Recipe
#!/bin/bash
# Install script for SQLite
# Version: 3.47.2

set -e

VERSION="3.47.2"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://www.sqlite.org/2024/sqlite-autoconf-${VERSION}.tar.gz
tar xzf sqlite-autoconf-${VERSION}.tar.gz
cd sqlite-autoconf-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --enable-dynamic-extensions
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/sqlite-autoconf-${VERSION}
