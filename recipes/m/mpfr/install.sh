#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-mpfr}"
mkdir -p "$SCRATCH"

URL="https://ftp.gnu.org/gnu/mpfr/mpfr-4.2.1.tar.gz"
VERSION="4.2.1"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
