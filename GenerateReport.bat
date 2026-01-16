@echo off
setlocal

REM -----------------------------------------
REM 1. Move to the directory of this script
REM -----------------------------------------
cd /d "%~dp0"

REM -----------------------------------------
REM 2. Activate the virtual environment
REM  
REM -----------------------------------------
call WSOR_NV_env\Scripts\activate.bat


REM -----------------------------------------
REM 3. Run your Python entry point
REM -----------------------------------------
python main.py

REM -----------------------------------------
REM 4. Pause so the window stays open
REM -----------------------------------------
echo.
echo Script finished. Press any key to exit.
pause >nul
