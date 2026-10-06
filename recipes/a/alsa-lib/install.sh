#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-alsa-lib}"
mkdir -p "$SCRATCH"

URL="https://www.alsa-project.org/files/pub/lib/alsa-lib-1.2.14.tar.bz2"
VERSION="1.2.14"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xjf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
