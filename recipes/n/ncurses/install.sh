#!/bin/bash
set -e

SCRATCH="${1:-ncurses}"
mkdir -p "$SCRATCH"

URL="https://ftp.gnu.org/gnu/ncurses/ncurses-6.5.tar.gz"
VERSION="6.5"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
