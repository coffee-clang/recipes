#!/bin/bash
set -e

SCRATCH="${1:-cryptsetup}"
mkdir -p "$SCRATCH"

URL="https://gitlab.com/cryptsetup/cryptsetup/-/archive/v2.7.5/cryptsetup-v2.7.5.tar.gz"
VERSION="2.7.5"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
