#!/bin/bash
set -e

SCRATCH="${1:-netpbm}"
mkdir -p "$SCRATCH"

URL="https://sourceforge.net/projects/netpbm/advanced/11.0.0/netpbm-11.0.0.tgz"
VERSION="11.0.0"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
