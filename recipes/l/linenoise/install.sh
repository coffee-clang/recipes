#!/bin/bash
set -e

PACKAGE="linenoise"
URL="https://github.com/antirez/linenoise/archive/refs/tags/1.0.tar.gz"
VERSION="1.0"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
