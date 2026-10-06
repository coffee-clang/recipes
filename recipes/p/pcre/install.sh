#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-pcre}"
mkdir -p "$SCRATCH"

URL="https://sourceforge.net/projects/pcre/files/pcre/8.45/pcre-8.45.tar.gz"
VERSION="8.45"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
