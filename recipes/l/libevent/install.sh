#!/bin/bash
set -e -o pipefail -u

PACKAGE="libevent"
URL="https://github.com/libevent/libevent/releases/download/release-2.1.13/libevent-2.1.13.tar.gz"
VERSION="2.1.13"
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
