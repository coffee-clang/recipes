#!/bin/bash
set -e

SCRATCH="${1:-alsa-lib}"
mkdir -p "$SCRATCH"

URL="https://www.alsa-project.org/files/pub/lib/alsa-lib-1.2.14.tar.bz2"
VERSION="1.2.14"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xjf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
