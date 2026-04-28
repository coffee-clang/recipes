#!/bin/bash
set -e

PACKAGE="qrencode"
URL="https://github.com/fukuchi/libqrencode/archive/refs/tags/v4.1.1.tar.gz"
VERSION="4.1.1"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
