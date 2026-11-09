#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "sds-$VERSION"
# Upstream ships no library build or install target.
cc -O2 -fPIC -c sds.c -o sds.o
cc -shared -o libsds.so sds.o
ar rcs libsds.a sds.o
install -D -m 644 sds.h "$PREFIX/include/sds.h"
install -D -m 644 sdsalloc.h "$PREFIX/include/sdsalloc.h"
install -D -m 755 libsds.so "$PREFIX/lib/libsds.so"
install -D -m 644 libsds.a "$PREFIX/lib/libsds.a"
