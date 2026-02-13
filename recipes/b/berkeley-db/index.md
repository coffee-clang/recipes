Title: berkeley-db
Date: 2026-02-12

# berkeley-db

## Version
6.2.32

## Description
Oracle Berkeley DB is an embedded database library providing key-value storage with transactions, locking, and recovery. It is widely used as a backend for directories, caches, and application data storage.

## Dependencies
- java (optional, for Java API)

## Recipe
#!/bin/bash
# Install script for Berkeley DB
# Version: 6.2.32

set -e

VERSION="6.2.32"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://download.oracle.com/berkeley-db/db-${VERSION}.tar.gz
tar xzf db-${VERSION}.tar.gz
cd db-${VERSION}/build_unix

../dist/configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/db-${VERSION}
