#!/bin/bash
set -e

SCRATCH="${1:-zstd}"
mkdir -p "$SCRATCH"

GITURL="https://github.com/facebook/zstd.git"
VERSION="1.5.6"
BRANCH="v1.5.6"

cd /tmp
git clone --depth 1 --branch "$BRANCH" "$GITURL"
rm -rf "$SCRATCH/zstd"
mv "zstd" "$SCRATCH/"
