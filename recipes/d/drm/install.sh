#!/bin/bash
set -e

SCRATCH="${1:-drm}"
mkdir -p "$SCRATCH"

URL="https://dri.freedesktop.org/libdrm/libdrm-2.4.120.tar.gz"
VERSION="2.4.120"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
