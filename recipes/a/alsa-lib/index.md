Title: alsa-lib
Date: 2026-02-12

# alsa-lib

## Version
1.2.14

## Description
The Advanced Linux Sound Architecture (ALSA) library provides audio and MIDI functionality for Linux. It is the core library for audio playback and recording, used by most Linux audio applications including PulseAudio, JACK, and many others.

## Dependencies
- ncurses (for alsaconf optional)
- python3 (for tools)

## Recipe
#!/bin/bash
# Install script for alsa-lib
# Version: 1.2.14

set -e

VERSION="1.2.14"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://www.alsa-project.org/files/pub/lib/alsa-lib-${VERSION}.tar.bz2
tar xjf alsa-lib-${VERSION}.tar.bz2
cd alsa-lib-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/alsa-lib-${VERSION} /tmp/alsa-lib-${VERSION}.tar.bz2
