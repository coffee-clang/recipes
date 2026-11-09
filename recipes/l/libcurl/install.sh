#!/bin/bash
set -e -o pipefail -u

ARCHIVE="$(basename "$URL")"
wget -q "$URL"
tar xzf "$ARCHIVE" --no-same-owner
cd "curl-$VERSION"
./configure --prefix="$PREFIX" --with-openssl --with-zlib --with-zstd \
    --with-brotli --with-nghttp2 --with-libidn2 --with-libpsl \
    --without-libssh2 --without-libssh --without-libgsasl --without-librtmp \
    --without-gssapi --without-nghttp3 --without-ngtcp2 --without-quiche \
    --without-msh3 --disable-ldap --disable-ldaps --disable-docs
make -j"$(nproc)"
make install
