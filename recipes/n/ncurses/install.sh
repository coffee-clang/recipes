#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-ncurses}"
mkdir -p "$SCRATCH"

URL="https://ftp.gnu.org/gnu/ncurses/ncurses-6.5.tar.gz"
VERSION="6.5"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
