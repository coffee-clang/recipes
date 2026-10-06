#!/bin/bash
set -e -o pipefail -u

PACKAGE="wavpack"
GITURL="https://github.com/dbry/WavPack.git"
VERSION="5.7.0"
BRANCH="5.7.0"

# Github package
COFFEE_HOME="${COFFEE_HOME:-$HOME/.coffee}"
PREFIX="$COFFEE_HOME/$PACKAGE/$VERSION"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
git clone --depth 1 --branch "$BRANCH" "$GITURL" "$PACKAGE"
rm -rf "$PREFIX"
mv "$PACKAGE" "$PREFIX"
