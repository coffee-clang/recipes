#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "pcre2-$VERSION"
cmake -S . -B build -DCMAKE_INSTALL_LIBDIR=lib -DCMAKE_INSTALL_PREFIX="$PREFIX" \
    -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON \
    -DPCRE2_SUPPORT_LIBREADLINE=ON -DPCRE2_SUPPORT_LIBEDIT=OFF \
    -DPCRE2_SUPPORT_LIBZ=ON -DPCRE2_SUPPORT_LIBBZ2=ON
cmake --build build -j"$(nproc)"
cmake --install build
