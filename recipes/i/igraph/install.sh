#!/bin/bash
set -e

PACKAGE="igraph"
URL="https://github.com/igraph/igraph/releases/download/0.10.15/igraph-0.10.15.tar.gz"
VERSION="0.10.15"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
