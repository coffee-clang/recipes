#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "hello-world-$VERSION"
# Upstream's Makefile builds only a static library and has no install target.
make libhello.a CFLAGS="-Wall -Wextra -O2 -fPIC"
gcc -shared -fPIC -O2 -o libhello.so hello.c
install -D -m 644 hello.h "$PREFIX/include/hello.h"
install -D -m 644 libhello.a "$PREFIX/lib/libhello.a"
install -D -m 755 libhello.so "$PREFIX/lib/libhello.so"
