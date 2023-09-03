@echo off

pause

:: Check for admin rights
echo Checking for admin rights...
net session >nul 2>&1

if %errorlevel% NEQ 0 (
    echo Attempting to elevate...
    :: powershell -Command "Start-Process cmd -ArgumentList '/c cd %~dp0 && %0' -Verb RunAs"
    powershell -Command "Start-Process cmd -ArgumentList '/c %~dp0\runDownload.bat' -Verb RunAs"

    echo Exiting...
    pause
    exit /b
) else (
    echo Running with admin rights...
    pause
)

pause

:: Run the Python script
python download.py
pause
