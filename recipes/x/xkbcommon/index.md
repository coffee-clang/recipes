Title: xkbcommon
Date: 2026-02-12

# xkbcommon

## Version
1.5.0

## Description
xkbcommon is a keyboard handling library providing a portable way to process key codes and compose keymaps. It is the modern replacement for X11 keyboard handling and is used by Wayland compositors.

## Dependencies
- libxcb (optional)

## License
MIT

## Recipe
#!/bin/bash
# Install script for xkbcommon
# Version: 1.5.0

set -e

VERSION="1.5.0"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/xkbcommon/libxkbcommon/archive/refs/tags/xkbcommon-${VERSION}.tar.gz
tar xzf xkbcommon-${VERSION}.tar.gz
cd libxkbcommon-xkbcommon-${VERSION}

meson setup build --prefix="$PREFIX" -Ddocs=false -Dx11=false
meson compile -C build
sudo meson install -C build

rm -rf /tmp/libxkbcommon-xkbcommon-${VERSION}
