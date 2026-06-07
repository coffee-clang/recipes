#!/bin/bash
set -e

PACKAGE="criterion"
VERSION="2.4.3"
URL="https://github.com/Snaipe/Criterion/archive/refs/tags/v${VERSION}.tar.gz"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"

cd "$PREFIX/Criterion-${VERSION}"
meson setup build --prefix="$PREFIX"
ninja -C build
meson install -C build
