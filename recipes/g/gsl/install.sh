#!/bin/bash
set -e

SCRATCH="${1:-gsl}"
mkdir -p "$SCRATCH"

URL="https://ftp.gnu.org/gnu/gsl/gsl-2.8.tar.gz"
VERSION="2.8"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
