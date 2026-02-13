#!/bin/bash
set -e

SCRATCH="${1:-openssl}"
mkdir -p "$SCRATCH"

URL="https://github.com/openssl/openssl/releases/download/openssl-3.4.1/openssl-3.4.1.tar.gz"
VERSION="3.4.1"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
