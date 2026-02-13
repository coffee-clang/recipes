Title: readline
Date: 2026-02-12

# readline

## Version
8.2

## Description
GNU Readline is a library for interactive command-line editing. It provides line editing, history, and completion features used by bash, gdb, and other interactive command-line programs.

## Dependencies
- ncurses (for terminal support)

## Recipe
#!/bin/bash
# Install script for readline
# Version: 8.2

set -e

VERSION="8.2"
PREFIX="${PREFIX:-/usr/local}"

cd /tmp
wget -q https://ftp.gnu.org/gnu/readline/readline-${VERSION}.tar.gz
tar xzf readline-${VERSION}.tar.gz
cd readline-${VERSION}

./configure --prefix="$PREFIX" --libdir="$PREFIX/lib"
make -j$(nproc)
sudo make install
sudo ldconfig

rm -rf /tmp/readline-${VERSION}
