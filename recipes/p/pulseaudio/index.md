Title: pulseaudio
Date: 2026-02-12

# pulseaudio

## Version
17.0

## Description
PulseAudio is a sound server providing advanced features including per-application volume control, switching between audio devices, and network audio. It is the default sound server for most Linux desktop environments.

## Dependencies
- glib

## License
LGPL-2.1
- libsndfile
- dbus

## Recipe
#!/bin/bash
# Install script for PulseAudio
# Version: 17.0

set -e

VERSION="17.0"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://freedesktop.org/software/pulseaudio/releases/pulseaudio-${VERSION}.tar.xz
tar xf pulseaudio-${VERSION}.tar.xz
cd pulseaudio-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --disable-zeroconf --disable-jack
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/pulseaudio-${VERSION}
