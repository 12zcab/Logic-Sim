@echo off
setlocal enabledelayedexpansion
<<<<<<< HEAD

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install nuitka zstandard

nuitka --standalone --include-package-data=Source Source/app.py
=======
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
>>>>>>> ee2d2a7aaa7e4854b77d51b1f7d7262c6d58e924
