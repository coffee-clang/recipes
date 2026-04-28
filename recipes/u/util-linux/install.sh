#!/bin/bash
set -e

PACKAGE="util-linux"
URL="https://github.com/karelzak/util-linux/archive/refs/tags/v2.40.2.tar.gz"
VERSION="2.40.2"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
