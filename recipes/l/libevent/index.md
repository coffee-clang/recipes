Title: libevent
Date: 2026-02-12

# libevent

## Version
2.1.13

## Description
libevent is an event notification library for developing scalable network servers. It provides a mechanism to execute a callback function when a specific event occurs on a file descriptor or after a timeout.

## Dependencies
- openssl (optional)

## License
MIT

## Recipe
#!/bin/bash
# Install script for libevent
# Version: 2.1.13

set -e

VERSION="2.1.13"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/libevent/libevent/releases/download/release-${VERSION}/libevent-${VERSION}.tar.gz
tar xzf libevent-${VERSION}.tar.gz
cd libevent-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --enable-openssl
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/libevent-${VERSION}
