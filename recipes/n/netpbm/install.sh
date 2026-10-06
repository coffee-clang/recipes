#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-netpbm}"
mkdir -p "$SCRATCH"

URL="https://sourceforge.net/projects/netpbm/advanced/11.0.0/netpbm-11.0.0.tgz"
VERSION="11.0.0"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
