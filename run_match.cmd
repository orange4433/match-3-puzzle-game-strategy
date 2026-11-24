@echo off
setlocal
cd /d "%~dp0"
python run_match.py %*
if errorlevel 1 (
    echo.
    echo Match could not finish. Read the message above.
    pause
)
