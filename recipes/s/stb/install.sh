#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
# The archive's top directory is named after the pinned commit.
mkdir -p "$PREFIX/include"
cp stb-*/stb_*.h "$PREFIX/include/"
