#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "libqrencode-$VERSION"
# CMakeLists.txt asks for a CMake version that CMake 4 no longer accepts.
cmake -S . -B build -DCMAKE_INSTALL_LIBDIR=lib -DCMAKE_INSTALL_PREFIX="$PREFIX" \
    -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5
cmake --build build -j"$(nproc)"
cmake --install build
