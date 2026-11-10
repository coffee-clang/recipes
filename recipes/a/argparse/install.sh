#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "argparse-$VERSION"
# Upstream's Makefile has no install target.
make
install -D -m 644 argparse.h "$PREFIX/include/argparse.h"
install -D -m 755 libargparse.so "$PREFIX/lib/libargparse.so"
install -D -m 644 libargparse.a "$PREFIX/lib/libargparse.a"
