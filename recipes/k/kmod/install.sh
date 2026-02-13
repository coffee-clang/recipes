#!/bin/bash
set -e

SCRATCH="${1:-kmod}"
mkdir -p "$SCRATCH"

URL="https://www.kernel.org/pub/linux/utils/kernel/kmod/kmod-33.tar.gz"
VERSION="33"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
