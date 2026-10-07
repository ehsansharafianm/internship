#!/usr/bin/env bash
# Rebuild the master cover-letter preview and PDF on macOS.
# Double-click in Finder (macOS) or run from a terminal.
# This is the macOS equivalent of Render-Master.cmd.

DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "Python 3 was not found. Install it from https://www.python.org/downloads/ and try again."
  exit 1
fi

"$PY" "$DIR/system/coverletter_tool.py" migrate --quiet
"$PY" "$DIR/system/coverletter_tool.py" render-master "$@"
exit $?
