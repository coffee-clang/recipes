#!/bin/bash
set -e

SCRATCH="${1:-hello-world}"
mkdir -p "$SCRATCH"

URL="https://github.com/coffee-clang/hello-world/archive/refs/tags/1.0.tar.gz"
VERSION="1.0"
ARCHIVE="hello-world-${VERSION}.tar.gz"

cd /tmp
wget -q "$URL"
tar xf "$ARCHIVE" -C "$SCRATCH"
cd "$SCRATCH/hello-world-${VERSION}"
make
