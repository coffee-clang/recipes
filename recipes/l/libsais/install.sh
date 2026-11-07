#!/bin/bash
set -e -o pipefail -u

PACKAGE="libsais"
URL="https://github.com/IlyaGrebnov/libsais/archive/refs/tags/v2.12.1.tar.gz"
VERSION="2.12.1"
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
cd "$PREFIX/libsais-${VERSION}"
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX="$PREFIX" -DLIBSAIS_BUILD_SHARED_LIB=ON
make
make install
