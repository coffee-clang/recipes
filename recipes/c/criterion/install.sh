#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xJf "$ARCHIVE" --no-same-owner
cd "criterion-$VERSION"
# The release tarball vendors debugbreak, klib, boxfort, nanomsg and nanopb,
# which have no recipes. nodownload builds those from the tarball but never
# fetches anything; libgit2 and libffi come from the registry.
meson setup build --wrap-mode=nodownload --prefix="$PREFIX" --libdir=lib --buildtype=release
meson compile -C build
meson install -C build
