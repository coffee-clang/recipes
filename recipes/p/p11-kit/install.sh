#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "p11-kit-$VERSION"
meson setup build --wrap-mode=nodownload --prefix="$PREFIX" --libdir=lib --buildtype=release \
    -Dlibffi=enabled -Dtrust_module=enabled -Dtrust_paths= \
    -Dsystemd=disabled -Dbash_completion=disabled -Dzsh_completion=disabled \
    -Dgtk_doc=false -Dman=false -Dnls=false -Dtest=false
meson compile -C build
meson install -C build
