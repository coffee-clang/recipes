#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-tiff}"
mkdir -p "$SCRATCH"

URL="https://download.osgeo.org/libtiff/tiff-4.7.0.tar.gz"
VERSION="4.7.0"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
