#!/bin/bash
set -e

PACKAGE="sds"
URL="https://github.com/antirez/sds/archive/refs/tags/2.0.0.tar.gz"
VERSION="2.0.0"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
