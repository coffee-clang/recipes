#!/bin/bash
set -e

PACKAGE="openssl"
URL="https://github.com/openssl/openssl/releases/download/openssl-3.4.1/openssl-3.4.1.tar.gz"
VERSION="3.4.1"
ARCHIVE="$(basename "$URL")"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
