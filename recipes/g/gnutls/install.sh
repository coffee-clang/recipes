#!/bin/bash
set -e -o pipefail -u

PACKAGE="gnutls"
URL="https://www.gnupg.org/ftp/gcrypt/gnutls/v3.8/gnutls-3.8.9.tar.xz"
VERSION="3.8.9"
ARCHIVE="$(basename "$URL")"

COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
mkdir -p "$PREFIX"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xJf "$ARCHIVE" --no-same-owner -C "$PREFIX"
rm -f "$ARCHIVE"
