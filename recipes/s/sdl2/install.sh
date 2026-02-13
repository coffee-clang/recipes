#!/bin/bash
set -e

SCRATCH="${1:-sdl2}"
mkdir -p "$SCRATCH"

URL="https://github.com/libsdl-org/SDL/releases/download/release-2.30.10/SDL2-2.30.10.tar.gz"
VERSION="2.30.10"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
