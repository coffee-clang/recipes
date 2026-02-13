#!/bin/bash
set -e

SCRATCH="${1:-libjpeg-turbo}"
mkdir -p "$SCRATCH"

URL="https://sourceforge.net/projects/libjpeg-turbo/files/3.0.4/libjpeg-turbo-3.0.4.tar.gz"
VERSION="3.0.4"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
