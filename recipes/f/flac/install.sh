#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xJf "$ARCHIVE" --no-same-owner
cd "flac-$VERSION"
./configure --prefix="$PREFIX" --disable-doxygen-docs --disable-examples
make -j"$(nproc)"
make install
