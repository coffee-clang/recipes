#!/bin/bash
set -e

SCRATCH="${1:-popt}"
mkdir -p "$SCRATCH"

URL="https://github.com/rpm-software-management/popt/releases/download/popt-1.19/popt-1.19.tar.gz"
VERSION="1.19"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
