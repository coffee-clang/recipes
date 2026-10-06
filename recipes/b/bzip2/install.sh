#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-bzip2}"
mkdir -p "$SCRATCH"

URL="https://sourceware.org/pub/bzip2/bzip2-1.0.8.tar.gz"
VERSION="1.0.8"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
