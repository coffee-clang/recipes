#!/bin/bash
set -e

PACKAGE="hiredis"
URL="https://github.com/redis/hiredis/archive/refs/tags/v1.2.0.tar.gz"
VERSION="1.2.0"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
cd "$PREFIX/hiredis-${VERSION}"
make
