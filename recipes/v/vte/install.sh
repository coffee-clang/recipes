#!/bin/bash
set -e

SCRATCH="${1:-vte}"
mkdir -p "$SCRATCH"

URL="https://gitlab.gnome.org/GNOME/vte/-/archive/0.76.3/vte-0.76.3.tar.gz"
VERSION="0.76.3"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
