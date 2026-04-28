#!/bin/bash
set -e

PACKAGE="fribidi"
URL="https://github.com/fribidi/fribidi/releases/download/v1.0.16/fribidi-1.0.16.tar.gz"
VERSION="1.0.16"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
