#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "argtable3-$VERSION"
cmake -S . -B build -DCMAKE_INSTALL_PREFIX="$PREFIX" -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=ON -DARGTABLE3_ENABLE_TESTS=OFF \
    -DARGTABLE3_ENABLE_EXAMPLES=OFF
cmake --build build -j"$(nproc)"
cmake --install build
