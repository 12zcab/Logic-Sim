@echo off
setlocal enabledelayedexpansion
python -m pip install -r requirements.txt
python -m pip install nuitka zstandard
if exist "bootstrap.exe" del /f /q "bootstrap.exe"
if exist "bootstrap.dist" rmdir /s /q "bootstrap.dist"
if exist "bootstrap.build" rmdir /s /q "bootstrap.build"
python -m nuitka ^
    --standalone ^
    --enable-plugin=tk-inter ^
    --include-package=yowasp_yosys ^
    --include-package=wasmtime ^
    --include-package=tkinter ^
    --remove-output ^
    bootstrap.py
