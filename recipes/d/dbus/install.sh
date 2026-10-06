#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-dbus}"
mkdir -p "$SCRATCH"

URL="https://dbus.freedesktop.org/releases/dbus/dbus-1.16.0.tar.gz"
VERSION="1.16.0"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
