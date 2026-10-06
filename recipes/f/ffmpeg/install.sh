#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-ffmpeg}"
mkdir -p "$SCRATCH"

URL="https://ffmpeg.org/releases/ffmpeg-7.1.1.tar.xz"
VERSION="7.1.1"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
