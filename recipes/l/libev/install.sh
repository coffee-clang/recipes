#!/bin/bash
set -e -o pipefail -u

PACKAGE="libev"
URL="https://dist.schmorp.de/libev/libev-4.33.tar.gz"
VERSION="4.33"
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
