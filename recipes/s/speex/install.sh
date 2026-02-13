#!/bin/bash
set -e

SCRATCH="${1:-speex}"
mkdir -p "$SCRATCH"

URL="https://downloads.xiph.org/releases/speex/speex-1.2.1.tar.gz"
VERSION="1.2.1"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
