#!/bin/bash
set -e -o pipefail -u

PACKAGE="fribidi"
URL="https://github.com/fribidi/fribidi/releases/download/v1.0.16/fribidi-1.0.16.tar.gz"
VERSION="1.0.16"
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
