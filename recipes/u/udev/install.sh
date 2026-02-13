#!/bin/bash
set -e

SCRATCH="${1:-udev}"
mkdir -p "$SCRATCH"

URL="https://github.com/systemd/systemd/archive/refs/tags/v257.4.tar.gz"
VERSION="257.4"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
