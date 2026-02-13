Title: fuse
Date: 2026-02-12

# fuse

## Version
3.16.2

## Description
FUSE (Filesystem in Userspace) allows users to create filesystems without kernel modifications. It enables developers to implement filesystems in user space, used by sshfs, gvfs, and many virtual filesystems.

## Dependencies
- libtool

## License
GPL-2.0

## Recipe
#!/bin/bash
# Install script for FUSE
# Version: 3.16.2

set -e

VERSION="3.16.2"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://github.com/libfuse/libfuse/releases/download/fuse-${VERSION}/fuse-${VERSION}.tar.gz
tar xzf fuse-${VERSION}.tar.gz
cd fuse-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --disable-util-mount
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/fuse-${VERSION}
