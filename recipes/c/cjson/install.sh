#!/bin/bash
set -e

SCRATCH="${1:-cjson}"
mkdir -p "$SCRATCH"

GITURL="https://github.com/DaveGamble/cJSON.git"
VERSION="1.7.18"
BRANCH="1.7.18"

cd /tmp
git clone --depth 1 --branch "$BRANCH" "$GITURL"
rm -rf "$SCRATCH/cjson"
mv "cjson" "$SCRATCH/"
