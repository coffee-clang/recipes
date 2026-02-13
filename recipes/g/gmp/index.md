Title: gmp
Date: 2026-02-12

# gmp

## Version
6.3.0

## Description
GMP (GNU Multiple Precision Arithmetic Library) is a free library for arbitrary precision arithmetic. It supports signed integers, rational numbers, and floating-point numbers with extremely high precision.

## Dependencies
- m4 (build requirement)

## Recipe
#!/bin/bash
# Install script for GMP
# Version: 6.3.0

set -e

VERSION="6.3.0"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://ftp.gnu.org/gnu/gmp/gmp-${VERSION}.tar.gz
tar xzf gmp-${VERSION}.tar.gz
cd gmp-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --enable-cxx
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/gmp-${VERSION}
