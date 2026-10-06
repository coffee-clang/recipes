#!/bin/bash
set -e -o pipefail -u

PACKAGE="stb"
URL="https://github.com/nothings/stb/archive/refs/heads/master.tar.gz"
VERSION="2024-12-01"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$PREFIX"
rm -f "$ARCHIVE"
# stb is header-only; headers are usable in-place
