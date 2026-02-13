Title: glib
Date: 2026-02-12

# glib

## Version
2.82.5

## Description
GLib is the core library of GTK+ and GNOME. It provides data structure handling, type casting, string utilities, file utilities, main loop, and other fundamental functionality used by most GNOME applications.

## Dependencies
- pcre2
- libffi

## Recipe
#!/bin/bash
# Install script for glib
# Version: 2.82.5

set -e

VERSION="2.82.5"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://download.gnome.org/sources/glib/${VERSION%.*}/glib-${VERSION}.tar.xz
tar xf glib-${VERSION}.tar.xz
cd glib-${VERSION}

meson setup build --prefix="$PREFIX" -Dtests=false -Dbsymbolic_functions=false
meson compile -C build
sudo meson install -C build

rm -rf /tmp/glib-${VERSION}
