#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-json-c}"
mkdir -p "$SCRATCH"

URL="https://s3.amazonaws.com/json-c_releases/releases/json-c-0.18.tar.gz"
VERSION="0.18"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
