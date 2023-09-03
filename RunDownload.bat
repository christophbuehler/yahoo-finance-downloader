@echo off

:: Check for admin rights and elevate if not present
net session >nul 2>&1
if %errorlevel% NEQ 0 (
    powershell -Command "Start-Process cmd -ArgumentList '/c cd %~dp0 && %0' -Verb RunAs"
    exit /b
)
pause

:: Run your Python script
python download.py

pause