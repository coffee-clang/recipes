#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "linenoise-$VERSION"
# Upstream ships no library build or install target.
cc -O2 -fPIC -c linenoise.c -o linenoise.o
cc -shared -o liblinenoise.so linenoise.o
ar rcs liblinenoise.a linenoise.o
install -D -m 644 linenoise.h "$PREFIX/include/linenoise.h"
install -D -m 755 liblinenoise.so "$PREFIX/lib/liblinenoise.so"
install -D -m 644 liblinenoise.a "$PREFIX/lib/liblinenoise.a"
