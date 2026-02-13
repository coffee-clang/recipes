Title: fribidi
Date: 2026-02-12

# fribidi

## Version
1.0.16

## Description
FriBidi is a free implementation of the Unicode Bidirectional Algorithm. It is used for rendering text in right-to-left languages (Arabic, Hebrew) and is required for proper text display in many applications.

## Dependencies
- meson or cmake

## License
LGPL-2.1

## Recipe
#!/bin/bash
# Install script for FriBidi
# Version: 1.0.16

set -e

VERSION="1.0.16"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/fribidi/fribidi/releases/download/v${VERSION}/fribidi-${VERSION}.tar.gz
tar xzf fribidi-${VERSION}.tar.gz
cd fribidi-${VERSION}

meson setup build --prefix="$PREFIX" -Ddocs=false
meson compile -C build
sudo meson install -C build

rm -rf /tmp/fribidi-${VERSION}
