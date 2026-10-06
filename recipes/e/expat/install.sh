#!/bin/bash
set -e -o pipefail -u

PACKAGE="expat"
VERSION="2.6.4"
URL="https://github.com/libexpat/libexpat/releases/download/R_${VERSION//./_}/expat-2.6.4.tar.gz"
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
