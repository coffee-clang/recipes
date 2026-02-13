Title: gsl
Date: 2026-02-12

# gsl

## Version
2.8

## Description
GNU Scientific Library (GSL) is a numerical library for C and C++ providing a wide range of mathematical functions including random number generators, linear algebra, fast Fourier transforms, and root finding.

## Dependencies
- None (self-contained)

## Recipe
#!/bin/bash
# Install script for GSL
# Version: 2.8

set -e

VERSION="2.8"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://ftp.gnu.org/gnu/gsl/gsl-${VERSION}.tar.gz
tar xzf gsl-${VERSION}.tar.gz
cd gsl-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/gsl-${VERSION}
