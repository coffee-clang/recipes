#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-gsl}"
mkdir -p "$SCRATCH"

URL="https://ftp.gnu.org/gnu/gsl/gsl-2.8.tar.gz"
VERSION="2.8"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
