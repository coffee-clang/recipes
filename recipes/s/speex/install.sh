#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-speex}"
mkdir -p "$SCRATCH"

URL="https://downloads.xiph.org/releases/speex/speex-1.2.1.tar.gz"
VERSION="1.2.1"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
