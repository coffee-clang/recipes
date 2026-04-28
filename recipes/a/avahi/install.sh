#!/bin/bash
set -e

PACKAGE="avahi"
URL="https://github.com/lathiat/avahi/releases/download/v0.9/avahi-0.9.tar.gz"
VERSION="0.9"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
