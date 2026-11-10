#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "gnutls-$VERSION"
./configure --prefix="$PREFIX" --with-p11-kit --with-idn \
    --without-tpm --without-tpm2 --disable-doc --disable-tests
make -j"$(nproc)"
make install
