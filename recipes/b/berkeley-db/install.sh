#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-berkeley-db}"
mkdir -p "$SCRATCH"

URL="https://download.oracle.com/berkeley-db/db-6.2.32.tar.gz"
VERSION="6.2.32"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
