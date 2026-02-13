#!/bin/bash
set -e

SCRATCH="${1:-icu}"
mkdir -p "$SCRATCH"

URL="https://github.com/unicode-org/icu/releases/download/release-${VERSION//./-}/icu4c-${VERSION//./_}-src.tgz"
VERSION="76.1"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
