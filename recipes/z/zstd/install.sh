#!/bin/bash
set -e -o pipefail -u

PACKAGE="zstd"
GITURL="https://github.com/facebook/zstd.git"
VERSION="1.5.6"
BRANCH="v1.5.6"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
git clone --depth 1 --branch "$BRANCH" "$GITURL" "$PACKAGE"
rm -rf "$PREFIX"
mv "$PACKAGE" "$PREFIX"
