#!/bin/bash
set -e -o pipefail -u

PACKAGE="hello-world"
URL="https://github.com/coffee-clang/hello-world/archive/refs/tags/1.0.tar.gz"
VERSION="1.0"
ARCHIVE="hello-world-${VERSION}.tar.gz"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL" -O "$ARCHIVE"
tar xf "$ARCHIVE" --no-same-owner -C "$PREFIX"
rm -f "$ARCHIVE"
cd "$PREFIX/hello-world-${VERSION}"
make
