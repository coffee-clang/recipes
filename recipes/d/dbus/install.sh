#!/bin/bash
set -e

SCRATCH="${1:-dbus}"
mkdir -p "$SCRATCH"

URL="https://dbus.freedesktop.org/releases/dbus/dbus-1.16.0.tar.gz"
VERSION="1.16.0"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
