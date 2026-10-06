#!/bin/bash
set -e -o pipefail -u

PACKAGE="icu"
VERSION="76.1"
URL="https://github.com/unicode-org/icu/releases/download/release-${VERSION//./-}/icu4c-${VERSION//./_}-src.tgz"
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
