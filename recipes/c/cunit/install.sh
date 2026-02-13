#!/bin/bash
set -e

SCRATCH="${1:-cunit}"
mkdir -p "$SCRATCH"

URL="https://sourceforge.net/projects/cunit/files/CUnit/2.1-3/CUnit-2.1-3.tar.bz2"
VERSION="2.1-3"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xjf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
