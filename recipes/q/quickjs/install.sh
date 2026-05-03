#!/bin/bash
set -e

PACKAGE="quickjs"
URL="https://bellard.org/quickjs/quickjs-2025-09-13-2.tar.xz"
VERSION="2025-09-13"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
