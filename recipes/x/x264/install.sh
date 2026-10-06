#!/bin/bash
set -e -o pipefail -u

PACKAGE="x264"
VERSION="r3222"
SHA="b35605ace3ddf7c1a5d67a2eb553f034aef41d55"
URL="https://code.videolan.org/videolan/x264/-/archive/$SHA/x264-$SHA.tar.gz"
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
# Shared and PIC: consumers such as FFmpeg link against a shared libx264.
./configure --prefix="$PREFIX" --enable-shared --enable-pic
make
make install
