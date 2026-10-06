#!/bin/bash
set -e -o pipefail -u

PACKAGE="cjson"
GITURL="https://github.com/DaveGamble/cJSON.git"
VERSION="1.7.18"
BRANCH="v1.7.18"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
git clone --depth 1 --branch "$BRANCH" "$GITURL" "$PACKAGE"
rm -rf "$PREFIX"
mv "$PACKAGE" "$PREFIX"
