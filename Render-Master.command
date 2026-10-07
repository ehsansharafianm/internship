#!/usr/bin/env bash
# Rebuild all master resumes on macOS.
# Double-click in Finder (macOS) or run from a terminal.
# This is the macOS equivalent of Render-Master.cmd.

DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "Python 3 was not found. Install it from https://www.python.org/downloads/ and try again."
  read -n 1 -s -r -p "Press any key to close this window..."
  echo ""
  exit 1
fi

"$PY" "$DIR/system/resume_tool.py" migrate --quiet
if "$PY" "$DIR/system/resume_tool.py" render-masters "$@"; then
  exit 0
fi

echo "Automatic PDF generation failed; generating HTML previews instead."
"$PY" "$DIR/system/resume_tool.py" render-masters -SkipPdf "$@"

exit $?
