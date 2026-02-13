Title: mpfr
Date: 2026-02-12

# mpfr

## Version
4.2.1

## Description
MPFR (Multiple Precision Floating-Point Rounding) is a C library for arbitrary-precision floating-point arithmetic. It extends GMP with accurate rounding and provides functions for high-precision calculations.

## Dependencies
- gmp

## Recipe
#!/bin/bash
# Install script for MPFR
# Version: 4.2.1

set -e

VERSION="4.2.1"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://ftp.gnu.org/gnu/mpfr/mpfr-${VERSION}.tar.gz
tar xzf mpfr-${VERSION}.tar.gz
cd mpfr-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --with-gmp="$PREFIX"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/mpfr-${VERSION}
