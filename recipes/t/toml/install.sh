#!/bin/bash
set -e

SCRATCH="${1:-toml}"
mkdir -p "$SCRATCH"

URL="https://github.com/cktan/tomlc17/archive/refs/tags/R260414.tar.gz"
VERSION="R260414"
ARCHIVE="$(basename "$URL")"

cd /tmp
wget -q "$URL"
tar xzf "$ARCHIVE" -C "$SCRATCH"
rm -f "$ARCHIVE"
