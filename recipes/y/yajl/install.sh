#!/bin/bash
set -e

PACKAGE="yajl"
URL="https://github.com/lloyd/yajl/archive/refs/tags/2.1.0.tar.gz"
VERSION="2.1.0"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
