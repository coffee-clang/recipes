Title: gtk
Date: 2026-02-12

# gtk

## Version
3.24.47

## Description
GTK (GIMP Toolkit) is a cross-platform GUI toolkit for creating graphical user interfaces. It is one of the most popular C GUI frameworks, used by GNOME applications, GIMP, Inkscape, and many other software.

## Dependencies
- glib

## License
LGPL-2.1
- cairo
- pango
- atk
- gdk-pixbuf

## Recipe
#!/bin/bash
# Install script for GTK+3
# Version: 3.24.47

set -e

VERSION="3.24.47"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://download.gnome.org/sources/gtk+/${VERSION%.*}/gtk+-${VERSION}.tar.xz
tar xf gtk+-${VERSION}.tar.xz
cd gtk+-${VERSION}

meson setup build --prefix="$PREFIX" -Dtests=false -Dwayland-backend=false
meson compile -C build
sudo meson install -C build

rm -rf /tmp/gtk+-${VERSION}
