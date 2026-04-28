#!/bin/bash
set -e

PACKAGE="toml"
URL="https://github.com/cktan/tomlc17/archive/refs/tags/R260414.tar.gz"
VERSION="R260414"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
