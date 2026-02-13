Title: libuv
Date: 2026-02-12

# libuv

## Version
1.49.2

## Description
libuv is a multi-platform support library for async I/O operations. It provides event loop, file system watching, networking, and threading primitives. It is the core of Node.js and used by many other projects.

## Dependencies
- cmake

## License
MIT

## Recipe
#!/bin/bash
# Install script for libuv
# Version: 1.49.2

set -e

VERSION="1.49.2"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://dist.libuv.org/dist/v${VERSION}/libuv-v${VERSION}.tar.gz
tar xzf libuv-v${VERSION}.tar.gz
cd libuv-v${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/libuv-v${VERSION}
