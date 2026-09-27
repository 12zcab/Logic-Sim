if exist "bootstrap.exe" del /f /q "bootstrap.exe"
if exist "internal_libs" rmdir /s /q "internal_libs"

python -m PyInstaller --onedir --contents-directory internal_libs --hidden-import=pkgutil --hidden-import=tabulate --hidden-import=typing --hidden-import=tempfile --hidden-import=json --hidden-import=keyboard --hidden-import=time --hidden-import=random --hidden-import=collections --collect-all yowasp_yosys --collect-all wasmtime --distpath . --workpath build_cache --specpath build_cache bootstrap.py

if exist "bootstrap" (
    move /y "bootstrap\bootstrap.exe" ".\"
    if exist "bootstrap\internal_libs" robocopy "bootstrap\internal_libs" "internal_libs" /e /move /ndl /nfl /njh /njs >nul
    rmdir /s /q "bootstrap"
)

pause
