#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "db-$VERSION/build_unix"
# Pre-C23 code: GCC 15 defaults to C23, where int (*)() means int (*)(void).
../dist/configure --prefix="$PREFIX" --libdir="$PREFIX/lib" CFLAGS="-O2 -std=gnu17"
make -j"$(nproc)"
make install
