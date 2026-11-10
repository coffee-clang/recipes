#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "readline-$VERSION"
./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --with-curses
make -j"$(nproc)" SHLIB_LIBS=-lncursesw
make install
