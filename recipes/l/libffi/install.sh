#!/bin/bash
set -e -o pipefail -u

PACKAGE="libffi"
URL="https://github.com/libffi/libffi/releases/download/v3.4.6/libffi-3.4.6.tar.gz"
VERSION="3.4.6"
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
# Autotools, not CMake: libffi's CMake build omits targets that wayland and
# criterion link against.
./configure --prefix="$PREFIX" --disable-multi-os-directory
make
make install
