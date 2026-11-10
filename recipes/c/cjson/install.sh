#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "cJSON-$VERSION"
# Upstream's Makefile races under -j.
make
# The Makefile reads LIBRARY_PATH and INCLUDE_PATH with ?=, so a value
# exported by the user's shell would redirect the install. Pin both.
make install PREFIX="$PREFIX" LIBRARY_PATH=lib INCLUDE_PATH=include/cjson
