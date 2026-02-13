#!/bin/bash
set -e

SCRATCH="${1:-bind}"
mkdir -p "$SCRATCH"

URL="https://downloads.isc.org/isc/bind9/9.18.28/bind-9.18.28.tar.gz"
VERSION="9.18.28"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
