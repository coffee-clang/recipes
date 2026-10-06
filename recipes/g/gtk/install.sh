#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-gtk}"
mkdir -p "$SCRATCH"

VERSION="3.24.47"
URL="https://download.gnome.org/sources/gtk+/${VERSION%.*}/gtk+-3.24.47.tar.xz"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
