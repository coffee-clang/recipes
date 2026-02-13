#!/bin/bash
set -e

SCRATCH="${1:-pulseaudio}"
mkdir -p "$SCRATCH"

URL="https://freedesktop.org/software/pulseaudio/releases/pulseaudio-17.0.tar.xz"
VERSION="17.0"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
