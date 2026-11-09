#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "bzip2-$VERSION"
# The default Makefile builds only the static library; the shared one has its
# own Makefile and no install target.
make -j"$(nproc)" -f Makefile-libbz2_so
make install PREFIX="$PREFIX"
install -m 755 "libbz2.so.$VERSION" "$PREFIX/lib/"
ln -sf "libbz2.so.$VERSION" "$PREFIX/lib/libbz2.so.1.0"
ln -sf libbz2.so.1.0 "$PREFIX/lib/libbz2.so"
