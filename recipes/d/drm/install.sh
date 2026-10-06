#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-drm}"
mkdir -p "$SCRATCH"

URL="https://dri.freedesktop.org/libdrm/libdrm-2.4.120.tar.gz"
VERSION="2.4.120"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
