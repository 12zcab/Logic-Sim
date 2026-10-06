python -m pip install -r requirements.txt
if exist "bootstrap.exe" del /f /q "bootstrap.exe"
if exist "internal_libs" rmdir /s /q "internal_libs"
if exist "build_cache" rmdir /s /q "build_cache"
python -c "import sys, subprocess, re, pathlib; req_file = pathlib.Path('requirements.txt'); reqs = [re.split(r'[=<>!~]', line.strip())[0].strip().replace('-', '_') for line in req_file.read_text(encoding='utf-8').splitlines() if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('pyinstaller')] if req_file.exists() else []; hidden = [arg for pkg in reqs for arg in ('--hidden-import', pkg)]; cmd = [sys.executable, '-m', 'PyInstaller', '--onedir', '--contents-directory', 'internal_libs'] + hidden + ['--collect-all', 'yowasp_yosys', '--collect-all', 'wasmtime', '--distpath', '.', '--workpath', 'build_cache', '--specpath', 'build_cache', 'bootstrap.py']; subprocess.run(cmd, check=True)"
if exist "bootstrap" (
    move /y "bootstrap\bootstrap.exe" ".\" >nul
    if exist "bootstrap\internal_libs" robocopy "bootstrap\internal_libs" "internal_libs" /e /move /ndl /nfl /njh /njs >nul
    rmdir /s /q "bootstrap"
)
echo build complete
pause