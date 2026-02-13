Title: libcurl
Date: 2026-02-12

# libcurl

## Version
8.11.1

## Description
libcurl is a free, easy-to-use URL transfer library supporting HTTP, HTTPS, FTP, FTPS, SCP, SFTP, TFTP, DICT, TELNET, LDAP, POP3, IMAP, SMTP, RTSP, RTMP, and many other protocols. It is the most widely used C HTTP client library.

## Dependencies
- openssl
- zlib

## Recipe
#!/bin/bash
# Install script for libcurl
# Version: 8.11.1

set -e

VERSION="8.11.1"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://curl.se/download/curl-${VERSION}.tar.gz
tar xzf curl-${VERSION}.tar.gz
cd curl-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --with-openssl --without-libpsl
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/curl-${VERSION}
