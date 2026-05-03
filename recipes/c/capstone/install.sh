#!/bin/bash
set -e

PACKAGE="capstone"
URL="https://github.com/capstone-engine/capstone/archive/refs/tags/5.0.3.tar.gz"
VERSION="5.0.3"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
cd "$PREFIX/capstone-${VERSION}"
make
