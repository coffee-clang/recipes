#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-kmod}"
mkdir -p "$SCRATCH"

URL="https://www.kernel.org/pub/linux/utils/kernel/kmod/kmod-33.tar.gz"
VERSION="33"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
