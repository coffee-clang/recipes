#!/bin/bash
set -e -o pipefail -u

PACKAGE="toml"
URL="https://github.com/cktan/tomlc17/archive/refs/tags/R260414.tar.gz"
VERSION="R260414"
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
