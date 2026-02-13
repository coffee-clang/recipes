Title: udev
Date: 2026-02-12

# udev

## Version
257.4

## Description
udev is the device manager for the Linux kernel. It manages device nodes in /dev and handles all user-space events when devices are added or removed, essential for modern Linux systems.

## Dependencies
- glib

## License
GPL-2.0
- libkmod
- gzip

## Recipe
#!/bin/bash
# Install script for udev (systemd)
# Version: 257.4

set -e

VERSION="257.4"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/systemd/systemd/archive/refs/tags/v${VERSION}.tar.gz
tar xzf v${VERSION}.tar.gz
cd systemd-${VERSION}

meson setup build --prefix="$PREFIX" -Dmode=developer -Dlink-udev-shared=false
meson compile -C build
sudo meson install -C build

rm -rf /tmp/systemd-${VERSION}
