#!/bin/bash
set -e

PACKAGE="udev"
URL="https://github.com/systemd/systemd/archive/refs/tags/v257.4.tar.gz"
VERSION="257.4"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
