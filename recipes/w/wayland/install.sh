#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-wayland}"
mkdir -p "$SCRATCH"

URL="https://wayland.freedesktop.org/releases/wayland-1.23.0.tar.xz"
VERSION="1.23.0"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
