#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "libepoxy-$VERSION"
# libGL is dlopen()ed at runtime, so epoxy.pc must not require a host gl.pc.
sed -i "/gl_reqs += 'gl'/d" src/meson.build
# EGL would compile against the host's EGL headers: no registry recipe has them.
meson setup build --prefix="$PREFIX" --libdir=lib --buildtype=release --wrap-mode=nodownload \
    -Dglx=yes -Dx11=true -Degl=no -Dtests=false -Ddocs=false
meson compile -C build
meson install -C build
