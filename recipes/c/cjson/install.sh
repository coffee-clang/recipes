#!/bin/bash
set -e

PACKAGE="cjson"
GITURL="https://github.com/DaveGamble/cJSON.git"
VERSION="1.7.18"
BRANCH="1.7.18"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
cd /tmp
git clone --depth 1 --branch "$BRANCH" "$GITURL"
rm -rf "$PREFIX"
mv "$PACKAGE" "$PREFIX"
