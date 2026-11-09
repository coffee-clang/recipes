#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "pcre-$VERSION"
./configure --prefix="$PREFIX"
make -j"$(nproc)"
make install
