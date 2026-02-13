Title: ffmpeg
Date: 2026-02-12

# ffmpeg

## Version
7.1.1

## Description
FFmpeg is the leading multimedia framework for encoding, decoding, transcoding, muxing, demuxing, streaming, and playing virtually all formats. It includes libavcodec, libavutil, libavformat, libavfilter, and other libraries.

## Dependencies
- libx264
- libx265
- libvpx
- libmp3lame
- libopus

## Recipe
#!/bin/bash
# Install script for FFmpeg
# Version: 7.1.1

set -e

VERSION="7.1.1"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://ffmpeg.org/releases/ffmpeg-${VERSION}.tar.xz
tar xf ffmpeg-${VERSION}.tar.xz
cd ffmpeg-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --enable-gpl --enable-nonfree
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/ffmpeg-${VERSION}
