#!/bin/bash
set -e -o pipefail -u

PACKAGE="simde"
URL="https://github.com/simd-everywhere/simde/archive/refs/tags/v0.8.2.tar.gz"
VERSION="0.8.2"
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

# Header-only library: copy simde/ to include/
mkdir -p "$PREFIX/include"
cp -r "$PREFIX/simde-${VERSION}/simde" "$PREFIX/include/"
rm -rf "$PREFIX/simde-${VERSION}"
