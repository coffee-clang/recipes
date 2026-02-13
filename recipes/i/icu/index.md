Title: icu
Date: 2026-02-12

# icu

## Version
76.1

## Description
ICU (International Components for Unicode) provides Unicode and globalization support including character properties, text boundary analysis, collation, normalization, date/time/number/currency formatting, and message formatting.

## Dependencies
- None (self-contained)

## Recipe
#!/bin/bash
# Install script for ICU
# Version: 76.1

set -e

VERSION="76.1"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/unicode-org/icu/releases/download/release-${VERSION//./-}/icu4c-${VERSION//./_}-src.tgz
tar xzf icu4c-${VERSION//./_}-src.tgz
cd icu/source

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/icu
