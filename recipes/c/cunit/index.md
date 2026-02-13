Title: cunit
Date: 2026-02-12

# cunit

## Version
2.1-3

## Description
CUnit is a lightweight unit testing framework for C. It provides a simple API for writing test cases, test suites, and test runners, inspired by JUnit and other unit testing frameworks.

## Dependencies
- None (minimal dependencies)

## License
GPL-2.0

## Recipe
#!/bin/bash
# Install script for CUnit
# Version: 2.1-3

set -e

VERSION="2.1-3"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://sourceforge.net/projects/cunit/files/CUnit/${VERSION}/CUnit-${VERSION}.tar.bz2
tar xjf CUnit-${VERSION}.tar.bz2
cd CUnit-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/CUnit-${VERSION}
