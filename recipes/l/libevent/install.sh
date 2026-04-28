#!/bin/bash
set -e

PACKAGE="libevent"
URL="https://github.com/libevent/libevent/releases/download/release-2.1.13/libevent-2.1.13.tar.gz"
VERSION="2.1.13"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
