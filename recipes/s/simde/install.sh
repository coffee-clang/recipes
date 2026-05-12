#!/bin/bash
set -e

PACKAGE="simde"
URL="https://github.com/simd-everywhere/simde/archive/refs/tags/v0.8.2.tar.gz"
VERSION="0.8.2"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"

# Header-only library: copy simde/ to include/
mkdir -p "$PREFIX/include"
cp -r "$PREFIX/simde-${VERSION}/simde" "$PREFIX/include/"
rm -rf "$PREFIX/simde-${VERSION}"
