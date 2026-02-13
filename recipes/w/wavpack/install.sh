#!/bin/bash
set -e

SCRATCH="${1:-wavpack}"
mkdir -p "$SCRATCH"

GITURL="https://github.com/dbry/WavPack.git"
VERSION="5.7.0"
BRANCH="5.7.0"

cd /tmp
git clone --depth 1 --branch "$BRANCH" "$GITURL"
rm -rf "$SCRATCH/wavpack"
mv "wavpack" "$SCRATCH/"
