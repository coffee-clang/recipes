#!/bin/bash
set -e

PACKAGE="xkbcommon"
URL="https://github.com/xkbcommon/libxkbcommon/archive/refs/tags/xkbcommon-1.5.0.tar.gz"
VERSION="1.5.0"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
