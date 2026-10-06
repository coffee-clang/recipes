#!/bin/bash
set -e -o pipefail -u

PACKAGE="criterion"
VERSION="2.4.3"
URL="https://github.com/Snaipe/Criterion/archive/refs/tags/v${VERSION}.tar.gz"
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

cd "$PREFIX/Criterion-${VERSION}"
meson setup build --prefix="$PREFIX"
ninja -C build
meson install -C build
