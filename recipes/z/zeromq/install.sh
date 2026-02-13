#!/bin/bash
set -e

SCRATCH="${1:-zeromq}"
mkdir -p "$SCRATCH"

URL="https://github.com/zeromq/libzmq/releases/download/v4.3.5/zeromq-4.3.5.tar.gz"
VERSION="4.3.5"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
