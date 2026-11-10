#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "quickjs-$VERSION"
make -j"$(nproc)"
make install PREFIX="$PREFIX"
