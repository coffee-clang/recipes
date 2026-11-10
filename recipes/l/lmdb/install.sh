#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "lmdb-LMDB_$VERSION/libraries/liblmdb"
make -j"$(nproc)"
make install prefix="$PREFIX"
