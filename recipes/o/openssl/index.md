Title: openssl
Date: 2026-02-12

# openssl

## Version
3.4.1

## Description
OpenSSL is a robust, full-featured toolkit for SSL/TLS protocols and general-purpose cryptography. It provides the libssl and libcrypto libraries implementing encryption, digital signatures, and certificate handling.

## Dependencies
- perl (for build)
- ca-certificates (for verification)

## Recipe
#!/bin/bash
# Install script for OpenSSL
# Version: 3.4.1

set -e

VERSION="3.4.1"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/openssl/openssl/releases/download/openssl-${VERSION}/openssl-${VERSION}.tar.gz
tar xzf openssl-${VERSION}.tar.gz
cd openssl-${VERSION}

./Configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --openssldir="$PREFIX/etc/ssl"
make -j$(nproc)
sudo make install_sw install_ssldirs
sudo ldconfig

rm -rf /tmp/openssl-${VERSION}
