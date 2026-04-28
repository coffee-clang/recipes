#!/bin/bash
set -e

PACKAGE="brotli"
GITURL="https://github.com/google/brotli.git"
VERSION="1.1.0"
BRANCH="v1.1.0"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
cd /tmp
git clone --depth 1 --branch "$BRANCH" "$GITURL"
rm -rf "$PREFIX"
mv "$PACKAGE" "$PREFIX"
