#!/bin/bash
set -e

SCRATCH="${1:-ffmpeg}"
mkdir -p "$SCRATCH"

URL="https://ffmpeg.org/releases/ffmpeg-7.1.1.tar.xz"
VERSION="7.1.1"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
