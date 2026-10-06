#!/bin/bash
set -e -o pipefail -u

PACKAGE="xorgproto"
URL="https://www.x.org/releases/individual/proto/xorgproto-2024.1.tar.gz"
VERSION="2024.1"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX/src"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$PREFIX/src"
rm -f "$ARCHIVE"
cd "$PREFIX"/src/*/
./configure --prefix="$PREFIX"
make
make install
