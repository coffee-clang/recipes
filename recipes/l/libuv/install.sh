#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-libuv}"
mkdir -p "$SCRATCH"

URL="https://dist.libuv.org/dist/v1.49.2/libuv-v1.49.2.tar.gz"
VERSION="1.49.2"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
