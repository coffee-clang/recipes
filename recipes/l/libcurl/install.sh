#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-libcurl}"
mkdir -p "$SCRATCH"

URL="https://curl.se/download/curl-8.11.1.tar.gz"
VERSION="8.11.1"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
