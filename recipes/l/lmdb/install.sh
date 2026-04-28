#!/bin/bash
set -e

PACKAGE="lmdb"
URL="https://github.com/LMDB/lmdb/archive/refs/tags/LMDB_0.9.33.tar.gz"
VERSION="0.9.33"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
