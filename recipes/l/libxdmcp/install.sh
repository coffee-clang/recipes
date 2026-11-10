#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "libXdmcp-$VERSION"
./configure --prefix="$PREFIX" --disable-docs --without-lint
make -j"$(nproc)"
make install
