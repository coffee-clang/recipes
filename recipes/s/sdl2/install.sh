#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "SDL2-$VERSION"
# X11 and ALSA are linked, not dlopen()ed, so they resolve to the registry's
# libraries. Backends with no buildable recipe (Wayland needs xkbcommon, KMSDRM
# needs Mesa's gbm, libudev needs gperf) are off, as are the other sound servers.
cmake -S . -B build -DCMAKE_INSTALL_LIBDIR=lib -DCMAKE_INSTALL_PREFIX="$PREFIX" \
    -DCMAKE_BUILD_TYPE=Release -DSDL_TESTS=OFF \
    -DSDL_X11=ON -DSDL_X11_SHARED=OFF -DSDL_X11_XSCRNSAVER=OFF \
    -DSDL_ALSA=ON -DSDL_ALSA_SHARED=OFF \
    -DSDL_WAYLAND=OFF -DSDL_KMSDRM=OFF -DSDL_RPI=OFF -DSDL_LIBUDEV=OFF -DSDL_IBUS=OFF \
    -DSDL_PIPEWIRE=OFF -DSDL_JACK=OFF -DSDL_ESD=OFF -DSDL_ARTS=OFF -DSDL_NAS=OFF \
    -DSDL_SNDIO=OFF -DSDL_LIBSAMPLERATE=OFF
cmake --build build -j"$(nproc)"
cmake --install build
