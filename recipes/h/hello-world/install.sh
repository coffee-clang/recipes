#!/bin/bash
set -e

PACKAGE="hello-world"
URL="https://github.com/coffee-clang/hello-world/archive/refs/tags/1.0.tar.gz"
VERSION="1.0"
ARCHIVE="hello-world-${VERSION}.tar.gz"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL" -O "$ARCHIVE"
tar xf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
cd "$PREFIX/hello-world-${VERSION}"
make
