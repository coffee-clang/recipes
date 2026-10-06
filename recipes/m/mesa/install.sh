#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-mesa}"
mkdir -p "$SCRATCH"

URL="https://archive.mesa3d.org/mesa-24.3.4.tar.xz"
VERSION="24.3.4"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
