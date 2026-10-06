#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-x11}"
mkdir -p "$SCRATCH"

URL="https://x.org/archive/individual/lib/libX11-1.8.9.tar.xz"
VERSION="1.8.9"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
