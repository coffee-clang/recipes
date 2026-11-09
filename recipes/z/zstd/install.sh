#!/bin/bash
set -e -o pipefail -u

git clone --depth 1 --branch "v$VERSION" "$URL" "$PACKAGE"
cd "$PACKAGE"
make -j"$(nproc)" -C lib
make -C lib install PREFIX="$PREFIX" LIBDIR="$PREFIX/lib"
