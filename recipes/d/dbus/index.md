Title: dbus
Date: 2026-02-12

# dbus

## Version
1.16.0

## Description
D-Bus is a message bus system for inter-process communication in Linux desktop environments. It provides a simple way for applications to communicate with each other and the system, used by systemd, GNOME, and KDE.

## Dependencies
- expat
- libpthread

## Recipe
#!/bin/bash
# Install script for D-Bus
# Version: 1.16.0

set -e

VERSION="1.16.0"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://dbus.freedesktop.org/releases/dbus/dbus-${VERSION}.tar.gz
tar xzf dbus-${VERSION}.tar.gz
cd dbus-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --disable-systemd --disable-x11-autolaunch
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/dbus-${VERSION}
