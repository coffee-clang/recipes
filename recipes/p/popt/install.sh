#!/bin/bash
set -e

PACKAGE="popt"
URL="https://github.com/rpm-software-management/popt/releases/download/popt-1.19/popt-1.19.tar.gz"
VERSION="1.19"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
