#!/bin/bash
set -e -o pipefail -u

PACKAGE="quickjs"
URL="https://bellard.org/quickjs/quickjs-2025-09-13-2.tar.xz"
VERSION="2025-09-13"
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
