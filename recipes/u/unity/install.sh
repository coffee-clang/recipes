#!/bin/bash
set -e

SCRATCH="${1:-unity}"
mkdir -p "$SCRATCH"

VERSION="2.6.1"
URL="https://github.com/ThrowTheSwitch/Unity/archive/refs/tags/v${VERSION}.tar.gz"
ARCHIVE="Unity-${VERSION}.tar.gz"

cd /tmp
wget -q "$URL" -O "$ARCHIVE"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
