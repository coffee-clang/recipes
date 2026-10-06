#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-cryptsetup}"
mkdir -p "$SCRATCH"

URL="https://gitlab.com/cryptsetup/cryptsetup/-/archive/v2.7.5/cryptsetup-v2.7.5.tar.gz"
VERSION="2.7.5"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
