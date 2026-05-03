#!/bin/bash
set -e

PACKAGE="uthash"
URL="https://github.com/troydhanson/uthash/archive/refs/tags/v2.3.0.tar.gz"
VERSION="2.3.0"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
