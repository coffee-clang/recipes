#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "mongoose-$VERSION"
# Upstream ships a single source file and no library build; build one here.
# The TLS backend changes struct layouts in mongoose.h, so it is fixed in
# library.toml's notes for consumers to match.
"${CC:-cc}" -O2 -fPIC -DMG_TLS=MG_TLS_BUILTIN -c mongoose.c -o mongoose.o
"${CC:-cc}" -shared -o libmongoose.so mongoose.o
ar rcs libmongoose.a mongoose.o
install -d "$PREFIX/include" "$PREFIX/lib"
install -m 644 mongoose.h "$PREFIX/include/"
install -m 644 libmongoose.a "$PREFIX/lib/"
install -m 755 libmongoose.so "$PREFIX/lib/"
