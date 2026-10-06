#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-liblzma}"
mkdir -p "$SCRATCH"

URL="https://tukaani.org/xz/xz-5.6.3.tar.gz"
VERSION="5.6.3"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
