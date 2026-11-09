#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xJf "$ARCHIVE" --no-same-owner
cd "libthai-$VERSION"
# The word-break dictionary is generated with libdatrie's trietool.
TRIETOOL="$(pkg-config --variable=prefix datrie-0.2)/bin/trietool"
./configure --prefix="$PREFIX" --disable-doxygen-doc TRIETOOL="$TRIETOOL"
make -j"$(nproc)"
make install
