#!/bin/bash
set -e -o pipefail -u

git clone --depth 1 --branch "$VERSION" "$URL" "$PACKAGE"
cd "$PACKAGE"
cmake -S . -B build -DCMAKE_INSTALL_PREFIX="$PREFIX" -DCMAKE_INSTALL_LIBDIR=lib -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON -DBUILD_TESTING=OFF -DWAVPACK_BUILD_PROGRAMS=OFF -DWAVPACK_BUILD_DOCS=OFF -DWAVPACK_INSTALL_DOCS=OFF
cmake --build build -j"$(nproc)"
cmake --install build
