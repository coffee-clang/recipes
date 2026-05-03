#!/bin/bash
set -e

PACKAGE="mongoose"
URL="https://github.com/cesanta/mongoose/archive/refs/tags/3.16.tar.gz"
VERSION="3.16"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
