Title: fftw3
Date: 2026-02-12

# fftw3

## Version
3.3.10

## Description
FFTW is a free, fast C library for computing the Discrete Fourier Transform (DFT). It is one of the fastest FFT implementations available, supporting 1D, 2D, and 3D transforms, and both real and complex data.

## Dependencies
- None (pure C library)

## License
GPL-2.0

## Recipe
#!/bin/bash
# Install script for FFTW
# Version: 3.3.10

set -e

VERSION="3.3.10"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://fftw.org/fftw-${VERSION}.tar.gz
tar xzf fftw-${VERSION}.tar.gz
cd fftw-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib" --enable-shared --enable-threads
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/fftw-${VERSION}
