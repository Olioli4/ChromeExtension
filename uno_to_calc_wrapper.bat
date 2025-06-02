@echo off
REM Wrapper to run main.py for native messaging
set PYTHONIOENCODING=utf-8
set SCRIPT_DIR=%~dp0
set PYTHON_EXE=python

REM If you use a venv, uncomment the next line and set the path
REM set PYTHON_EXE=%SCRIPT_DIR%venv\Scripts\python.exe

REM Use python from cache if available
where python >nul 2>nul
if %ERRORLEVEL%==0 (
    set PYTHON_EXE=python
) else (
    echo Python not found in PATH. Please install Python or update this script.
    exit /b 1
)

REM Ensure no _python_ folder is used for cache, use 'python' only
REM (No action needed, as only 'python' is used above)

%PYTHON_EXE% "%SCRIPT_DIR%main.py"
