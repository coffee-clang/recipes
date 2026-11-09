#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "gmp-$VERSION"
# GMP 6.3.0's configure probes are not valid C23 (GCC 15's default), so
# every compiler candidate is rejected. Pin the dialect via CC, which keeps
# the CFLAGS GMP picks for the host CPU.
./configure --prefix="$PREFIX" CC="${CC:-cc} -std=gnu17"
make -j"$(nproc)"
make install
