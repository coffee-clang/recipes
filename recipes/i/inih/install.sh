#!/bin/bash
set -e

PACKAGE="inih"
URL="https://github.com/benhoyt/inih/archive/refs/tags/r56.tar.gz"
VERSION="r56"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
