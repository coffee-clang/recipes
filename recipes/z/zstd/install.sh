#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "zstd-$VERSION"
make -j"$(nproc)" -C lib
make -C lib install PREFIX="$PREFIX" LIBDIR="$PREFIX/lib"
