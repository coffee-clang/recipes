#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-flac}"
mkdir -p "$SCRATCH"

URL="https://downloads.xiph.org/flac/flac-1.4.3.tar.xz"
VERSION="1.4.3"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
