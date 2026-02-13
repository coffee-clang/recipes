Title: zeromq
Date: 2026-02-12

# zeromq

## Version
4.3.5

## Description
ZeroMQ (0MQ) is a high-performance asynchronous messaging library providing a socket abstraction for various messaging patterns. It supports request-reply, publish-subscribe, and push-pull patterns across transports.

## Dependencies
- cmake
- libsodium (optional)

## Recipe
#!/bin/bash
# Install script for ZeroMQ
# Version: 4.3.5

set -e

VERSION="4.3.5"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/zeromq/libzmq/releases/download/v${VERSION}/zeromq-${VERSION}.tar.gz
tar xzf zeromq-${VERSION}.tar.gz
cd zeromq-${_VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/zeromq-${VERSION}
