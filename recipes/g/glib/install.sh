#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-glib}"
mkdir -p "$SCRATCH"

VERSION="2.82.5"
URL="https://download.gnome.org/sources/glib/${VERSION%.*}/glib-2.82.5.tar.xz"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
