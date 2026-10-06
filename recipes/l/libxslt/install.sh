#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-libxslt}"
mkdir -p "$SCRATCH"

VERSION="1.1.42"
URL="https://download.gnome.org/sources/libxslt/${VERSION%.*}/libxslt-1.1.42.tar.gz"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
