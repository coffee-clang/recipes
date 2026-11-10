#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "mesa-$VERSION"
# Minimal software-rendering build: softpipe, no LLVM, no Vulkan drivers.
meson setup build --prefix="$PREFIX" --libdir=lib --buildtype=release --wrap-mode=nodownload -Dplatforms=x11 -Dgallium-drivers=softpipe -Dvulkan-drivers= -Dllvm=disabled -Dglx=dri -Degl=enabled -Dgbm=enabled -Dglvnd=disabled -Dvalgrind=disabled -Dlibunwind=disabled -Dbuild-tests=false -Dzstd=disabled -Dlmsensors=disabled
meson compile -C build -j"$(nproc)"
meson install -C build
