#!/bin/bash
set -e

SCRATCH="${1:-libassuan}"
mkdir -p "$SCRATCH"

URL="https://gnupg.org/ftp/gcrypt/libassuan/libassuan-2.5.8.tar.bz2"
VERSION="2.5.8"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xjf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
