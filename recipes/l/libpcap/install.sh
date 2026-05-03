#!/bin/bash
set -e

PACKAGE="libpcap"
URL="https://www.tcpdump.org/release/libpcap-1.10.5.tar.gz"
VERSION="1.10.5"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$PREFIX"
rm -f "$ARCHIVE"
cd "$PREFIX/libpcap-${VERSION}"
./configure --prefix="$PREFIX"
make
make install
