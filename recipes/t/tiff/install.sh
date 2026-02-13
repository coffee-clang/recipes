#!/bin/bash
set -e

SCRATCH="${1:-tiff}"
mkdir -p "$SCRATCH"

URL="https://download.osgeo.org/libtiff/tiff-4.7.0.tar.gz"
VERSION="4.7.0"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
