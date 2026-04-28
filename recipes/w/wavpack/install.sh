#!/bin/bash
set -e

PACKAGE="wavpack"
GITURL="https://github.com/dbry/WavPack.git"
VERSION="5.7.0"
BRANCH="5.7.0"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
cd /tmp
git clone --depth 1 --branch "$BRANCH" "$GITURL"
rm -rf "$PREFIX"
mv "$PACKAGE" "$PREFIX"
