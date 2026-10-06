#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-pulseaudio}"
mkdir -p "$SCRATCH"

URL="https://freedesktop.org/software/pulseaudio/releases/pulseaudio-17.0.tar.xz"
VERSION="17.0"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
