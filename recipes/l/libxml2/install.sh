#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-libxml2}"
mkdir -p "$SCRATCH"

VERSION="2.12.9"
URL="https://download.gnome.org/sources/libxml2/${VERSION%.*}/libxml2-2.12.9.tar.gz"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
