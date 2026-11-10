#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "libsndfile-$VERSION"
# The bundled ALAC code defines its own bool, which C23 (GCC 15) rejects.
./configure --prefix="$PREFIX" --enable-external-libs --disable-mpeg \
    --disable-alsa --disable-sqlite --disable-full-suite \
    CFLAGS="-O2 -std=gnu17"
make -j"$(nproc)"
make install
