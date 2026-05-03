#!/bin/bash
set -e

PACKAGE="stb"
URL="https://github.com/nothings/stb/archive/refs/heads/master.tar.gz"
VERSION="2024-12-01"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
# stb is header-only; headers are usable in-place
