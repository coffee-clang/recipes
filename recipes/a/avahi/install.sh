#!/bin/bash
set -e

SCRATCH="${1:-avahi}"
mkdir -p "$SCRATCH"

URL="https://github.com/lathiat/avahi/releases/download/v0.9/avahi-0.9.tar.gz"
VERSION="0.9"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
