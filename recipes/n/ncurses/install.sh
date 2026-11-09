#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "ncurses-$VERSION"
# The .pc files would otherwise go to the host pkg-config directory.
# The C++ binding fails to compile with GCC 15; C consumers do not need it.
# configure takes the default terminfo directory from an exported TERMINFO,
# which would make install write to the host database: pin it under $PREFIX
# and keep the host databases on the search path.
./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" \
    --with-shared --without-debug --without-ada --without-tests \
    --without-cxx-binding \
    --enable-pc-files --with-pkg-config-libdir="$PREFIX/lib/pkgconfig" \
    --with-default-terminfo-dir="$PREFIX/share/terminfo" \
    --with-terminfo-dirs="$PREFIX/share/terminfo:/etc/terminfo:/lib/terminfo:/usr/share/terminfo"
make -j"$(nproc)"
make install
