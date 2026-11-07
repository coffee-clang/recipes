#!/bin/bash
set -e -o pipefail -u

PACKAGE="argparse"
URL="https://github.com/cofyc/argparse/archive/refs/tags/v1.1.0.tar.gz"
VERSION="1.1.0"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$PREFIX"
rm -f "$ARCHIVE"
cd "$PREFIX/argparse-${VERSION}"
# Upstream's Makefile has no install target.
make
install -D -m 644 argparse.h "$PREFIX/include/argparse.h"
install -D -m 755 libargparse.so "$PREFIX/lib/libargparse.so"
install -D -m 644 libargparse.a "$PREFIX/lib/libargparse.a"
