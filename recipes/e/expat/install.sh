#!/bin/bash
set -e

PACKAGE="expat"
VERSION="2.6.4"
URL="https://github.com/libexpat/libexpat/releases/download/R_${VERSION//./_}/expat-2.6.4.tar.gz"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
