#!/bin/bash
set -e

SCRATCH="${1:-acl}"
mkdir -p "$SCRATCH"

URL="https://download.savannah.nongnu.org/releases/acl/acl-2.3.2.tar.gz"
VERSION="2.3.2"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
