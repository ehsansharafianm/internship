@echo off
python "%~dp0system\resume_tool.py" migrate --quiet
python "%~dp0system\resume_tool.py" render-masters %*
