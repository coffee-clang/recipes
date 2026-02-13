#!/bin/bash
set -e

SCRATCH="${1:-blas}"
mkdir -p "$SCRATCH"

URL="https://www.netlib.org/blas/blas-3.12.0.tar.gz"
VERSION="3.12.0"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
