#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-opus}"
mkdir -p "$SCRATCH"

URL="https://archive.mozilla.org/pub/opus/opus-1.5.2.tar.gz"
VERSION="1.5.2"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
