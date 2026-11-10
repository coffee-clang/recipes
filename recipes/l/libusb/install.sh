#!/bin/bash
set -e -o pipefail -u

tar xjf "$ARCHIVE" --no-same-owner
cd "libusb-$VERSION"
# Without libudev, libusb detects hotplug events through netlink.
./configure --prefix="$PREFIX" --disable-udev
make -j"$(nproc)"
make install
