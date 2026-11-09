#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "lmdb-LMDB_$VERSION/libraries/liblmdb"
make -j"$(nproc)"
make install prefix="$PREFIX"
