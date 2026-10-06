#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-libassuan}"
mkdir -p "$SCRATCH"

URL="https://gnupg.org/ftp/gcrypt/libassuan/libassuan-2.5.8.tar.bz2"
VERSION="2.5.8"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xjf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
