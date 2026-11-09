#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd icu/source
./configure --prefix="$PREFIX" --disable-samples --disable-tests
make -j"$(nproc)"
make install
