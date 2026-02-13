#!/bin/bash
set -e

SCRATCH="${1:-wayland}"
mkdir -p "$SCRATCH"

URL="https://wayland.freedesktop.org/releases/wayland-1.23.0.tar.xz"
VERSION="1.23.0"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
