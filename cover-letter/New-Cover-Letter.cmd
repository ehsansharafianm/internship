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

"%PY%" "%~dp0system\coverletter_tool.py" migrate --quiet

if "%~1"=="" (
  "%PY%" "%~dp0system\coverletter_tool.py" wizard
) else (
  "%PY%" "%~dp0system\coverletter_tool.py" create %*
)
set "RC=%errorlevel%"

if not "%RC%"=="0" (
  echo.
  echo The command reported an error ^(code %RC%^). Read the messages above.
  pause
)
exit /b %RC%
