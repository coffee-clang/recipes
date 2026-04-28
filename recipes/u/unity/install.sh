#!/bin/bash
set -e

PACKAGE="unity"
VERSION="2.6.1"
URL="https://github.com/ThrowTheSwitch/Unity/archive/refs/tags/v${VERSION}.tar.gz"
ARCHIVE="Unity-${VERSION}.tar.gz"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL" -O "$ARCHIVE"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
