#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xjf "$ARCHIVE" --no-same-owner
cd "CUnit-$VERSION"
# The release tarball ships configure.in but no configure script.
autoreconf -fi
./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j"$(nproc)"
make install
