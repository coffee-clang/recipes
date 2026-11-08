#!/bin/bash
set -e -o pipefail -u

PACKAGE="wuffs"
URL="https://github.com/google/wuffs/archive/refs/tags/v0.3.6.tar.gz"
VERSION="0.3.6"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX/include"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
# wuffs is a single-file library: #define WUFFS_IMPLEMENTATION in one .c file
cp "wuffs-${VERSION}/release/c/wuffs-v0.3.c" "$PREFIX/include"
