#!/bin/bash
set -e -o pipefail -u

PACKAGE="harfbuzz"
URL="https://github.com/harfbuzz/harfbuzz/releases/download/10.0.1/harfbuzz-10.0.1.tar.xz"
VERSION="10.0.1"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xf "$ARCHIVE" --no-same-owner -C "$PREFIX"
rm -f "$ARCHIVE"
