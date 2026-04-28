#!/bin/bash
set -e

PACKAGE="jansson"
URL="https://github.com/akheron/jansson/releases/download/v2.14/jansson-2.14.tar.gz"
VERSION="2.14"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
