@echo off
setlocal enableextensions
cd /d "%~dp0"

rem --- Locate a Python 3 interpreter ---
set "PY="
where python >nul 2>&1 && set "PY=python"
if not defined PY (
  where py >nul 2>&1 && set "PY=py"
)
if not defined PY (
  if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python314\python.exe"
)
if not defined PY (
  for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do if exist "%%D\python.exe" set "PY=%%D\python.exe"
)
if not defined PY (
  echo.
  echo Python 3 was not found.
  echo Install it from https://www.python.org/downloads/ and tick
  echo "Add python.exe to PATH" during setup, then run this again.
  echo.
  pause
  exit /b 1
)

"%PY%" "%~dp0system\resume_tool.py" migrate --quiet
"%PY%" "%~dp0system\resume_tool.py" render-masters %*
set "RC=%errorlevel%"

echo.
pause
exit /b %RC%
