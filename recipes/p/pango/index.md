Title: pango
Date: 2026-02-12

# pango

## Version
1.54.0

## Description
Pango is a library for layout and rendering of internationalized text. It works with GTK+ to provide proper text rendering for complex scripts and is used by GNOME applications for internationalized text display.

## Dependencies
- glib

## License
LGPL-2.1
- cairo
- harfbuzz
- fontconfig

## Recipe
#!/bin/bash
# Install script for pango
# Version: 1.54.0

set -e

VERSION="1.54.0"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://download.gnome.org/sources/pango/${VERSION%.*}/pango-${VERSION}.tar.xz
tar xf pango-${VERSION}.tar.xz
cd pango-${VERSION}

meson setup build --prefix="$PREFIX" -Dtests=false
meson compile -C build
sudo meson install -C build

rm -rf /tmp/pango-${VERSION}
