@echo off
setlocal enabledelayedexpansion

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install nuitka zstandard

nuitka --standalone ^
       --remove-output ^
       --nofollow-import-to=*.test ^
       --nofollow-import-to=*.tests ^
       --include-package-data=Source ^
       Source/app.py