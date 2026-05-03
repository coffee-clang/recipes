#!/bin/bash
set -e

PACKAGE="cpu_features"
URL="https://github.com/google/cpu_features/archive/refs/tags/v0.9.0.tar.gz"
VERSION="0.9.0"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
cd "$PREFIX/cpu_features-${VERSION}"
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX="$PREFIX"
make
make install
