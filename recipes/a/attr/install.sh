#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-attr}"
mkdir -p "$SCRATCH"

URL="https://download.savannah.nongnu.org/releases/attr/attr-2.5.2.tar.gz"
VERSION="2.5.2"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
