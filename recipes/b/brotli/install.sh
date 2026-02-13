#!/bin/bash
set -e

SCRATCH="${1:-brotli}"
mkdir -p "$SCRATCH"

GITURL="https://github.com/google/brotli.git"
VERSION="1.1.0"
BRANCH="v1.1.0"

cd /tmp
git clone --depth 1 --branch "$BRANCH" "$GITURL"
rm -rf "$SCRATCH/brotli"
mv "brotli" "$SCRATCH/"
