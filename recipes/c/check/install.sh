#!/bin/bash
set -e

PACKAGE="check"
URL="https://github.com/libcheck/check/releases/download/0.15.2/check-0.15.2.tar.gz"
VERSION="0.15.2"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
