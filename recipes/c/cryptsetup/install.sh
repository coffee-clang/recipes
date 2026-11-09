#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xJf "$ARCHIVE" --no-same-owner
cd "cryptsetup-$VERSION"
./configure --prefix="$PREFIX" --with-crypto_backend=gcrypt --disable-asciidoc \
    --disable-ssh-token --disable-nls --disable-udev
make -j"$(nproc)"
make install
