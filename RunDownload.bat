@echo off

:: Check for admin rights and elevate if not present
net session >nul 2>&1
if %errorlevel% NEQ 0 (
    powershell -Command "Start-Process -Verb RunAs -FilePath '%0'"
    exit /b
)

pause

:: Run your Python script
python download.py

pause