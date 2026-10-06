#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-vte}"
mkdir -p "$SCRATCH"

URL="https://gitlab.gnome.org/GNOME/vte/-/archive/0.76.3/vte-0.76.3.tar.gz"
VERSION="0.76.3"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
