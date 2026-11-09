#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "netpbm-$VERSION"
# Netpbm has no prefix-aware install: configure through config.mk, stage the
# result with "make package", then copy the library parts into the prefix.
cp config.mk.in config.mk
cat >> config.mk <<'CONFIG'
CFLAGS_CONFIG = -std=gnu17
CFLAGS_SHLIB = -fPIC
JPEGLIB = libjpeg.so
LEX =
CONFIG
make -j"$(nproc)"
make package pkgdir="$PWD/pkg"
mkdir -p "$PREFIX/include" "$PREFIX/lib"
cp -R pkg/include/. "$PREFIX/include/"
cp -P pkg/lib/* pkg/sharedlink/* pkg/staticlink/* "$PREFIX/lib/"
