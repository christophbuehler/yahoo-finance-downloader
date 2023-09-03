@echo off
:: Check for admin rights
net session >nul 2>&1
if %errorlevel% NEQ 0 (
    powershell -Command "Start-Process cmd -ArgumentList '/c cd %~dp0 && %0' -Verb RunAs"
    exit /b
)

:: Run the Python script
python download.py
pause
