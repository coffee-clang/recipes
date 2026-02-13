#!/bin/bash
set -e

SCRATCH="${1:-lz4}"
mkdir -p "$SCRATCH"

GITURL="https://github.com/lz4/lz4.git"
VERSION="1.10.0"
BRANCH="v1.10.0"

cd /tmp
git clone --depth 1 --branch "$BRANCH" "$GITURL"
rm -rf "$SCRATCH/lz4"
mv "lz4" "$SCRATCH/"
