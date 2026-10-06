#!/bin/bash
set -e -o pipefail -u

PACKAGE="libpciaccess"
URL="https://gitlab.freedesktop.org/xorg/lib/libpciaccess/-/archive/libpciaccess-0.17/libpciaccess-0.17.tar.gz"
VERSION="0.17"
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
./autogen.sh
./configure --prefix="$PREFIX"
make
make install
