#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xJf "$ARCHIVE" --no-same-owner
cd "libXinerama-$VERSION"
./configure --prefix="$PREFIX"
make -j"$(nproc)"
make install
