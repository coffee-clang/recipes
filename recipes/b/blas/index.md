Title: blas
Date: 2026-02-12

# blas

## Version
3.12.0

## Description
BLAS (Basic Linear Algebra Subprograms) is a specification for linear algebra libraries. It provides low-level routines for vector and matrix operations, forming the foundation for more advanced numerical libraries like LAPACK.

## Dependencies
- gfortran (for reference implementation)

## Recipe
#!/bin/bash
# Install script for BLAS
# Version: 3.12.0

set -e

VERSION="3.12.0"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://www.netlib.org/blas/blas-${VERSION}.tar.gz
tar xzf blas-${VERSION}.tar.gz
cd BLAS-${VERSION}

gfortran -O3 -fPIC -c *.f
ar r libblas.a *.o
sudo cp libblas.a "$PREFIX/lib/"
sudo cp *.h "$PREFIX/include/"
sudo ldconfig

rm -rf /tmp/BLAS-${VERSION}
