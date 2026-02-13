#!/bin/bash
set -e

SCRATCH="${1:-atk}"
mkdir -p "$SCRATCH"

URL="https://download.gnome.org/sources/atk/${VERSION%.*}/atk-2.52.0.tar.xz"
VERSION="2.52.0"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
