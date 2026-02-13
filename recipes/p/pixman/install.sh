#!/bin/bash
set -e

SCRATCH="${1:-pixman}"
mkdir -p "$SCRATCH"

URL="https://cairographics.org/releases/pixman-0.44.2.tar.gz"
VERSION="0.44.2"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
