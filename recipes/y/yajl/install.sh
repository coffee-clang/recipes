#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
cd "yajl-$VERSION"
# Only the library: the tool/test subdirectories read the LOCATION target
# property, an error under CMake 4.
sed -i -E '/ADD_SUBDIRECTORY\((test|reformatter|verify|example|perf)\)/d' CMakeLists.txt
# Upstream requires CMake 2.6, which CMake 4 refuses without a policy floor.
cmake -S . -B build -DCMAKE_INSTALL_PREFIX="$PREFIX" -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_BUILD_TYPE=Release -DCMAKE_POLICY_VERSION_MINIMUM=3.5
cmake --build build -j"$(nproc)"
cmake --install build
