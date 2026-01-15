@echo off
setlocal EnableExtensions

echo ========================================
echo   Port Detector Pro - Build Script
echo ========================================
echo.

REM Check Python
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.11+ and add to PATH.
    pause
    exit /b 1
)

python --version

REM Check Nuitka
python -c "import nuitka" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing Nuitka...
    python -m pip install -U pip
    python -m pip install -U nuitka
)

REM Install deps
echo.
echo [1/3] Installing requirements...
python -m pip install -U pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] pip install failed.
    pause
    exit /b 1
)

REM Build (PyQt6)
echo.
echo [2/3] Building with Nuitka...
python -m nuitka --standalone --onefile --windows-console-mode=disable --enable-plugin=pyqt6 --include-qt-plugins=platforms --output-filename=PortDetector.exe --output-dir=dist --remove-output main.py
if errorlevel 1 (
    echo [ERROR] Build failed. Check output above.
    pause
    exit /b 1
)

echo.
echo [3/3] Done!
if exist "dist\PortDetector.exe" (
    echo SUCCESS: dist\PortDetector.exe
) else (
    echo [WARN] dist\PortDetector.exe not found.
)
echo.
pause
