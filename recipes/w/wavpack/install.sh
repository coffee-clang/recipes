#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "wavpack-$VERSION"
cmake -S . -B build -DCMAKE_INSTALL_PREFIX="$PREFIX" -DCMAKE_INSTALL_LIBDIR=lib -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON -DBUILD_TESTING=OFF -DWAVPACK_BUILD_PROGRAMS=OFF -DWAVPACK_BUILD_DOCS=OFF -DWAVPACK_INSTALL_DOCS=OFF
cmake --build build -j"$(nproc)"
cmake --install build
