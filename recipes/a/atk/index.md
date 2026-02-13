Title: atk
Date: 2026-02-12

# atk

## Version
2.52.0

## Description
ATK (Accessibility Toolkit) provides an interface for accessibility support. It is used by assistive technologies to interact with GTK and other GNOME applications, enabling screen readers and other accessibility tools.

## Dependencies
- glib
- gobject-introspection

## Recipe
#!/bin/bash
# Install script for atk
# Version: 2.52.0

set -e

VERSION="2.52.0"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://download.gnome.org/sources/atk/${VERSION%.*}/atk-${VERSION}.tar.xz
tar xf atk-${VERSION}.tar.xz
cd atk-${VERSION}

meson setup build --prefix="$PREFIX" -Dtests=false
meson compile -C build
sudo meson install -C build

rm -rf /tmp/atk-${VERSION} /tmp/atk-${VERSION}.tar.xz
