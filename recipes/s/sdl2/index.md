Title: sdl2
Date: 2026-02-12

# sdl2

## Version
2.30.10

## Description
SDL (Simple DirectMedia Layer) is a cross-platform library for multimedia and game development. It provides low-level access to audio, keyboard, mouse, joystick, and graphics hardware. SDL2 is the modern version with improved features.

## Dependencies
- libpulse (optional)
- alsa (optional)

## Recipe
#!/bin/bash
# Install script for SDL2
# Version: 2.30.10

set -e

VERSION="2.30.10"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/libsdl-org/SDL/releases/download/release-${VERSION}/SDL2-${VERSION}.tar.gz
tar xzf SDL2-${VERSION}.tar.gz
cd SDL2-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/SDL2-${VERSION}
