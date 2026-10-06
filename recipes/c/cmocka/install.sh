#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-cmocka}"
mkdir -p "$SCRATCH"

URL="https://git.cryptomilk.org/projects/cmocka.git/snapshot/cmocka-1.1.7.tar.gz"
VERSION="1.1.7"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
