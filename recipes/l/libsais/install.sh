#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "libsais-$VERSION"
# LIBSAIS_BUILD_SHARED_LIB defaults to OFF.
cmake -S . -B build -DCMAKE_INSTALL_PREFIX="$PREFIX" -DCMAKE_INSTALL_LIBDIR=lib -DLIBSAIS_BUILD_SHARED_LIB=ON
cmake --build build -j"$(nproc)"
cmake --install build
