Title: wayland
Date: 2026-02-12

# wayland

## Version
1.23.0

## Description
Wayland is a display server protocol and library implementation. It provides the communication between display server and clients, serving as the modern replacement for X11 on Linux desktops.

## Dependencies
- libffi

## License
MIT
- libxml2

## Recipe
#!/bin/bash
# Install script for Wayland
# Version: 1.23.0

set -e

VERSION="1.23.0"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://wayland.freedesktop.org/releases/wayland-${VERSION}.tar.xz
tar xf wayland-${VERSION}.tar.xz
cd wayland-${VERSION}

meson setup build --prefix="$PREFIX" -Ddocumentation=false
meson compile -C build
sudo meson install -C build

rm -rf /tmp/wayland-${VERSION}
