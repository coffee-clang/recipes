#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "fuse-$VERSION"
# Library only: the utilities install a setuid fusermount3 and udev rules.
meson setup build --wrap-mode=nofallback --prefix="$PREFIX" --libdir=lib --buildtype=release \
    -Dutils=false -Dexamples=false -Dtests=false
ninja -C build
ninja -C build install
