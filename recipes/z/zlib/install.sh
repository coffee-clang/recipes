#!/bin/bash
set -e

PACKAGE="zlib"
URL="https://github.com/madler/zlib/archive/refs/tags/v1.3.1.tar.gz"
VERSION="1.3.1"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
