#!/bin/bash
set -e

SCRATCH="${1:-readline}"
mkdir -p "$SCRATCH"

URL="https://ftp.gnu.org/gnu/readline/readline-8.2.tar.gz"
VERSION="8.2"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
