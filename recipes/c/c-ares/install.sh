#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cmake -S "c-ares-$VERSION" -B build -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_INSTALL_PREFIX="$PREFIX" -DCMAKE_BUILD_TYPE=Release \
    -DCARES_BUILD_TOOLS=OFF
cmake --build build -j"$(nproc)"
cmake --install build
