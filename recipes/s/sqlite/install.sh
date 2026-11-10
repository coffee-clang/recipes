#!/bin/bash
set -e -o pipefail -u

tar xzf "$ARCHIVE" --no-same-owner
# The top directory encodes the version as e.g. 3470200, so derive it.
cd "${ARCHIVE%.tar.gz}"
# The tgetent probe tries -ltermcap first and finds the host's; use ncursesw.
./configure --prefix="$PREFIX" ac_cv_search_tgetent=-lncursesw
make -j"$(nproc)"
make install
