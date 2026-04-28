#!/bin/bash
set -e

PACKAGE="zstd"
GITURL="https://github.com/facebook/zstd.git"
VERSION="1.5.6"
BRANCH="v1.5.6"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
cd /tmp
git clone --depth 1 --branch "$BRANCH" "$GITURL"
rm -rf "$PREFIX"
mv "$PACKAGE" "$PREFIX"
