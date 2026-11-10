#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "lapack-$VERSION"
# Reference BLAS has no C header: CBLAS provides cblas.h.
cmake -S . -B build -DCMAKE_INSTALL_PREFIX="$PREFIX" -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=ON -DCBLAS=ON -DLAPACKE=OFF -DBUILD_TESTING=OFF
cmake --build build -j"$(nproc)"
cmake --install build
