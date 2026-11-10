#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "kmod-$VERSION"
./configure --prefix="$PREFIX" --disable-manpages \
    --with-bashcompletiondir="$PREFIX/share/bash-completion/completions"
make -j"$(nproc)"
make install
