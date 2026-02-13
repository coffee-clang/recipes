Title: mesa
Date: 2026-02-12

# mesa

## Version
24.3.4

## Description
Mesa is an open-source implementation of the OpenGL, Vulkan, and other graphics APIs. It provides the graphics driver stack for open-source GPU drivers on Linux and is used by most desktop Linux distributions.

## Dependencies
- llvm
- libdrm
- glproto

## Recipe
#!/bin/bash
# Install script for Mesa
# Version: 24.3.4

set -e

VERSION="24.3.4"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://archive.mesa3d.org/mesa-${VERSION}.tar.xz
tar xf mesa-${VERSION}.tar.xz
cd mesa-${VERSION}

meson setup build --prefix="$PREFIX" -Dglx=disabled -Dplatforms=x11 -Dgallium-drivers=""
meson compile -C build
sudo meson install -C build

rm -rf /tmp/mesa-${VERSION}
