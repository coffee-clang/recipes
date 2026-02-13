#!/bin/bash
set -e

SCRATCH="${1:-libxml2}"
mkdir -p "$SCRATCH"

URL="https://download.gnome.org/sources/libxml2/${VERSION%.*}/libxml2-2.12.9.tar.gz"
VERSION="2.12.9"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
