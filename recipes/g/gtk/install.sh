#!/bin/bash
set -e

SCRATCH="${1:-gtk}"
mkdir -p "$SCRATCH"

URL="https://download.gnome.org/sources/gtk+/${VERSION%.*}/gtk+-3.24.47.tar.xz"
VERSION="3.24.47"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
