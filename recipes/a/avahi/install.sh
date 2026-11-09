#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "avahi-$VERSION"
# Only the client libraries: language bindings, GUI tools and docs are off so
# the build needs no extra host packages.
./configure --prefix="$PREFIX" --with-distro=none --disable-qt5 --disable-gtk3 \
    --disable-mono --disable-monodoc --disable-python --disable-pygobject \
    --disable-manpages --disable-xmltoman --disable-doxygen-doc --disable-gdbm \
    --disable-libdaemon --disable-libevent --disable-tests
make -j"$(nproc)"
make install
