Title: avahi
Date: 2026-02-12

# avahi

## Version
0.9

## Description
Avahi is a free, LGPL implementation of DNS Service Discovery (DNS-SD) for Linux. It allows applications to discover services on the local network without configuration, commonly used for printer and file sharing discovery.

## Dependencies
- glib

## License
LGPL-2.1
- expat
- libdaemon

## Recipe
#!/bin/bash
# Install script for avahi
# Version: 0.9

set -e

VERSION="0.9"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/lathiat/avahi/releases/download/v${VERSION}/avahi-${VERSION}.tar.gz
tar xzf avahi-${VERSION}.tar.gz
cd avahi-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --disable-mono --disable-python
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/avahi-${VERSION} /tmp/avahi-${VERSION}.tar.gz
