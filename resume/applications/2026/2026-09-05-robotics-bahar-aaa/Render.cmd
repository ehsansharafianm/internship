@echo off
python "%~dp0..\..\..\system\resume_tool.py" render -Input "%~dp0resume.yaml" -OutputHtml "%~dp0index.html" -OutputPdf "%~dp0resume.pdf" %*
