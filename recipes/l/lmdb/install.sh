#!/bin/bash
set -e -o pipefail -u

PACKAGE="lmdb"
URL="https://github.com/LMDB/lmdb/archive/refs/tags/LMDB_0.9.33.tar.gz"
VERSION="0.9.33"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$PREFIX"
rm -f "$ARCHIVE"
