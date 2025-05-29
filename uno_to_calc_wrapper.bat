@echo off
set "PYTHONPATH=%PYTHONPATH%;D:\Browsertocalc"
set "PYTHONIOENCODING=utf-8"
set "PYTHONPYCACHEPREFIX=D:\Browsertocalc\pycache"

echo %DATE% %TIME% Starting native host... >> "D:\Browsertocalc\native_host.log"

python "D:\Browsertocalc\uno_to_calc.py" >> "D:\Browsertocalc\native_host.log" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo %DATE% %TIME% Script failed with error %ERRORLEVEL% >> "D:\Browsertocalc\native_host.log"
    exit /b %ERRORLEVEL%
)
