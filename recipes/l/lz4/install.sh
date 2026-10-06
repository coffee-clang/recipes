#!/bin/bash
set -e -o pipefail -u

PACKAGE="lz4"
GITURL="https://github.com/lz4/lz4.git"
VERSION="1.10.0"
BRANCH="v1.10.0"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
git clone --depth 1 --branch "$BRANCH" "$GITURL" "$PACKAGE"
rm -rf "$PREFIX"
mv "$PACKAGE" "$PREFIX"
