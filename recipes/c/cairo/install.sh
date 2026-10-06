#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-cairo}"
mkdir -p "$SCRATCH"

URL="https://www.cairographics.org/releases/cairo-1.18.2.tar.xz"
VERSION="1.18.2"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
