#!/bin/bash
set -e -o pipefail -u

PACKAGE="unity"
VERSION="2.6.1"
URL="https://github.com/ThrowTheSwitch/Unity/archive/refs/tags/v${VERSION}.tar.gz"
ARCHIVE="Unity-${VERSION}.tar.gz"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL" -O "$ARCHIVE"
tar xzf "$ARCHIVE" --no-same-owner -C "$PREFIX"
rm -f "$ARCHIVE"
