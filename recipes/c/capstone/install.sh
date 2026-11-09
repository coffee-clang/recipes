#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "capstone-$VERSION"
cmake -S . -B build -DCMAKE_INSTALL_PREFIX="$PREFIX" -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=ON -DCAPSTONE_BUILD_TESTS=OFF \
    -DCAPSTONE_BUILD_CSTOOL=OFF
cmake --build build -j"$(nproc)"
cmake --install build
