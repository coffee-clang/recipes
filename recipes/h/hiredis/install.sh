#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "hiredis-$VERSION"
# The Makefile reads its install paths with ?= and bakes them into hiredis.pc
# at build time, so a value exported by the user's shell would redirect the
# install. Pin them on both commands.
make -j"$(nproc)" USE_SSL=1 PREFIX="$PREFIX" LIBRARY_PATH=lib \
    INCLUDE_PATH=include/hiredis PKGCONF_PATH=pkgconfig
make install USE_SSL=1 PREFIX="$PREFIX" LIBRARY_PATH=lib \
    INCLUDE_PATH=include/hiredis PKGCONF_PATH=pkgconfig
