#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-nettle}"
mkdir -p "$SCRATCH"

URL="https://ftp.gnu.org/gnu/nettle/nettle-3.10.tar.gz"
VERSION="3.10"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
