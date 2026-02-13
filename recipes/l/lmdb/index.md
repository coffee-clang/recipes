Title: lmdb
Date: 2026-02-12

# lmdb

## Version
0.9.33

## Description
LMDB (Lightning Memory-Mapped Database) is an embedded key-value database with ACID semantics. It uses memory-mapped files for high performance and is known for its simplicity and reliability.

## Dependencies
- None (self-contained)

## Recipe
#!/bin/bash
# Install script for LMDB
# Version: 0.9.33

set -e

VERSION="0.9.33"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/LMDB/lmdb/archive/refs/tags/LMDB_${VERSION}.tar.gz
tar xzf LMDB_${VERSION}.tar.gz
cd LMDB_LMDB_${VERSION}

make -j$(nproc)
sudo cp -r libraries/liblmdb "$PREFIX"
sudo cp -r libraries/lmdb.h "$PREFIX/include/"
sudo ldconfig

rm -rf /tmp/LMDB_LMDB_${VERSION}
