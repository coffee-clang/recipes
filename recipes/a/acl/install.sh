#!/bin/bash
set -e -o pipefail -u

SCRATCH="${1:-acl}"
mkdir -p "$SCRATCH"

URL="https://download.savannah.nongnu.org/releases/acl/acl-2.3.2.tar.gz"
VERSION="2.3.2"
ARCHIVE="$(basename "$URL")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner -C "$SCRATCH"
rm -f "$ARCHIVE"
