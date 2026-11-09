#!/bin/bash
set -e -o pipefail -u

git clone --depth 1 --branch "v$VERSION" "$URL" "$PACKAGE"
cd "$PACKAGE"
cmake -S . -B build -DCMAKE_INSTALL_PREFIX="$PREFIX" -DCMAKE_INSTALL_LIBDIR=lib -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON -DBROTLI_DISABLE_TESTS=ON
cmake --build build -j"$(nproc)"
cmake --install build
