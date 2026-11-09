#!/bin/bash
set -e -o pipefail -u

git clone --depth 1 --branch "v$VERSION" "$URL" "$PACKAGE"
cd "$PACKAGE"
# Upstream's Makefile races under -j.
make
# The Makefile reads LIBRARY_PATH and INCLUDE_PATH with ?=, so a value
# exported by the user's shell would redirect the install. Pin both.
make install PREFIX="$PREFIX" LIBRARY_PATH=lib INCLUDE_PATH=include/cjson
