#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-freetype}"
mkdir -p "$SCRATCH"

URL="https://download.savannah.nongnu.org/releases/freetype/freetype-2.13.3.tar.gz"
VERSION="2.13.3"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
