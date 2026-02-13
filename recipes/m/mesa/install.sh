#!/bin/bash
set -e

SCRATCH="${1:-mesa}"
mkdir -p "$SCRATCH"

URL="https://archive.mesa3d.org/mesa-24.3.4.tar.xz"
VERSION="24.3.4"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
