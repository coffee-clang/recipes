#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-readline}"
mkdir -p "$SCRATCH"

URL="https://ftp.gnu.org/gnu/readline/readline-8.2.tar.gz"
VERSION="8.2"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
