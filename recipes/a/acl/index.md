Title: acl
Date: 2026-02-12

# acl

## Version
2.3.2

## Description
The acl library provides utilities for manipulating Access Control Lists (ACLs) on files and directories. It is part of the POSIX.1e ACL implementation for Linux, allowing fine-grained permission management beyond traditional Unix file permissions.

## Dependencies
- attr (extended attributes library)

## Recipe
#!/bin/bash
# Install script for acl
# Version: 2.3.2

set -e

VERSION="2.3.2"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://download.savannah.nongnu.org/releases/acl/acl-${VERSION}.tar.gz
tar xzf acl-${VERSION}.tar.gz
cd acl-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/acl-${VERSION} /tmp/acl-${VERSION}.tar.gz
