#!/bin/bash
set -e -o pipefail -u

PACKAGE="libusb"
URL="https://github.com/libusb/libusb/releases/download/v1.0.27/libusb-1.0.27.tar.bz2"
VERSION="1.0.27"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xjf "$ARCHIVE" --no-same-owner -C "$PREFIX"
rm -f "$ARCHIVE"
cd "$PREFIX/libusb-${VERSION}"
./configure --prefix="$PREFIX"
make
make install
