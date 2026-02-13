Title: bind
Date: 2026-02-12

# bind

## Version
9.18.28

## Description
BIND (Berkeley Internet Name Domain) is the most widely used DNS server software on the Internet. The libdns library provides DNS protocol handling, resolution, and zone management capabilities.

## Dependencies
- openssl
- libuv
- zlib

## Recipe
#!/bin/bash
# Install script for bind (libdns)
# Version: 9.18.28

set -e

VERSION="9.18.28"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://downloads.isc.org/isc/bind9/${VERSION}/bind-${VERSION}.tar.gz
tar xzf bind-${VERSION}.tar.gz
cd bind-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --disable-fixed-rrset --disable-native-pkcs11
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/bind-${VERSION} /tmp/bind-${VERSION}.tar.gz
