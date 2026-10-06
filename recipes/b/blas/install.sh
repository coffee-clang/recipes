#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-blas}"
mkdir -p "$SCRATCH"

URL="https://www.netlib.org/blas/blas-3.12.0.tar.gz"
VERSION="3.12.0"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
