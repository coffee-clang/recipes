#!/bin/bash
set -e

SCRATCH="${1:-json-c}"
mkdir -p "$SCRATCH"

URL="https://s3.amazonaws.com/json-c_releases/releases/json-c-0.18.tar.gz"
VERSION="0.18"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
