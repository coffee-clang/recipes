#!/bin/bash
set -e -o pipefail -u

PACKAGE="libxcb"
URL="https://x.org/archive/individual/lib/libxcb-1.17.0.tar.xz"
VERSION="1.17.0"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX/src"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xJf "$ARCHIVE" --no-same-owner -C "$PREFIX/src"
rm -f "$ARCHIVE"
cd "$PREFIX"/src/*/
./configure --prefix="$PREFIX"
make
make install
