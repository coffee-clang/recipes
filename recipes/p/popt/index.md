Title: popt
Date: 2026-02-12

# popt

## Version
1.19

## Description
popt is a command-line option parsing library for C. It provides a convenient interface for parsing command-line arguments and is used by many applications including rpm and wget.

## Dependencies
- None (self-contained)

## Recipe
#!/bin/bash
# Install script for popt
# Version: 1.19

set -e

VERSION="1.19"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/rpm-software-management/popt/releases/download/popt-1.19/popt-${VERSION}.tar.gz
tar xzf popt-${VERSION}.tar.gz
cd popt-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/popt-${VERSION}
