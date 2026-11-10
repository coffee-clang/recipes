#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "tomlc17-$VERSION"
make -j"$(nproc)"
make install prefix="$PREFIX"
