#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-c-ares}"
mkdir -p "$SCRATCH"

URL="https://c-ares.org/download/c-ares-1.34.4.tar.gz"
VERSION="1.34.4"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
