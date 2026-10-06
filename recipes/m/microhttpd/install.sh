#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-microhttpd}"
mkdir -p "$SCRATCH"

URL="https://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-1.0.0.tar.gz"
VERSION="1.0.0"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
