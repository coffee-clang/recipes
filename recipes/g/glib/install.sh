#!/bin/bash
set -e

SCRATCH="${1:-glib}"
mkdir -p "$SCRATCH"

URL="https://download.gnome.org/sources/glib/${VERSION%.*}/glib-2.82.5.tar.xz"
VERSION="2.82.5"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
