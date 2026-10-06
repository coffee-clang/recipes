#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-sqlite}"
mkdir -p "$SCRATCH"

URL="https://www.sqlite.org/2024/sqlite-autoconf-3.47.2.tar.gz"
VERSION="3.47.2"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
