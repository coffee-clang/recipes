#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-pango}"
mkdir -p "$SCRATCH"

VERSION="1.54.0"
URL="https://download.gnome.org/sources/pango/${VERSION%.*}/pango-1.54.0.tar.xz"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
