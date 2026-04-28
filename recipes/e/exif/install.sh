#!/bin/bash
set -e

PACKAGE="exif"
URL="https://github.com/libexif/libexif/releases/download/v0.6.24/libexif-0.6.24.tar.gz"
VERSION="0.6.24"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
