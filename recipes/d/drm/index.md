Title: drm
Date: 2026-02-12

# drm

## Version
2.4.120

## Description
Direct Rendering Manager (DRM) provides user-space libraries for interfacing with graphics hardware. It is a kernel-user space interface for graphics drivers and is used by Mesa, X Server, and wayland compositors.

## Dependencies
- libdrm (userspace component)

## License
MIT
- kernel headers

## Recipe
#!/bin/bash
# Install script for libdrm
# Version: 2.4.120

set -e

VERSION="2.4.120"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://dri.freedesktop.org/libdrm/libdrm-${VERSION}.tar.gz
tar xzf libdrm-${VERSION}.tar.gz
cd libdrm-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --disable-udev
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/libdrm-${VERSION}
