#!/bin/bash
set -e

PACKAGE="glfw"
URL="https://github.com/glfw/glfw/archive/refs/tags/3.4.tar.gz"
VERSION="3.4"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
cd "$PREFIX/glfw-${VERSION}"
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX="$PREFIX"
make
make install
