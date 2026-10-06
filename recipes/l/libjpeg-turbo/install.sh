#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-libjpeg-turbo}"
mkdir -p "$SCRATCH"

URL="https://sourceforge.net/projects/libjpeg-turbo/files/3.0.4/libjpeg-turbo-3.0.4.tar.gz"
VERSION="3.0.4"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
