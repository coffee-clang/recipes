#!/bin/bash
set -e -o pipefail -u

PACKAGE="capstone"
URL="https://github.com/capstone-engine/capstone/archive/refs/tags/5.0.3.tar.gz"
VERSION="5.0.3"
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
cd "$PREFIX/capstone-${VERSION}"
make
