#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "libffi-$VERSION"
# --disable-multi-os-directory keeps the library in lib rather than lib64.
./configure --prefix="$PREFIX" --disable-multi-os-directory
make -j"$(nproc)"
make install
