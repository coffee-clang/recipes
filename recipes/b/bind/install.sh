#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-bind}"
mkdir -p "$SCRATCH"

URL="https://downloads.isc.org/isc/bind9/9.18.28/bind-9.18.28.tar.gz"
VERSION="9.18.28"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
