#!/bin/bash
set -e -o pipefail -u

tar xJf "$ARCHIVE" --no-same-owner
cd "libcap-$VERSION"
# Only the libraries: the tools and pam_cap are left out. lib= stops the
# Makefile from guessing lib64 from the host loader.
make -C libcap -j"$(nproc)" prefix="$PREFIX" lib=lib GOLANG=no PAM_CAP=no
make -C libcap install prefix="$PREFIX" lib=lib GOLANG=no PAM_CAP=no
