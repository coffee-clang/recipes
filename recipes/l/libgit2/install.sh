#!/bin/bash
set -e -o pipefail -u

PACKAGE="libgit2"
URL="https://github.com/libgit2/libgit2/archive/refs/tags/v1.8.4.tar.gz"
VERSION="1.8.4"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$PREFIX"
rm -f "$ARCHIVE"
cd "$PREFIX/libgit2-${VERSION}"
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX="$PREFIX"
make
make install
