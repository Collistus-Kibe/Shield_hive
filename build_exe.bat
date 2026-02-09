@echo off
REM ============================================================
REM Shield Hive - Hackathon Build Script
REM Creates standalone EXE for judges
REM ============================================================

echo.
echo ============================================================
echo   SHIELD HIVE - BUILD SYSTEM
echo   Creating Hackathon Submission Package...
echo ============================================================
echo.

REM Check for PyInstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [*] Installing PyInstaller...
    pip install pyinstaller
)

REM Clean previous builds
echo [*] Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Build the EXE using spec file
echo [*] Building ShieldHive_Server.exe...
pyinstaller shield_hive.spec --noconfirm

REM Check result
if exist "dist\ShieldHive_Server.exe" (
    echo.
    echo ============================================================
    echo   BUILD SUCCESSFUL!
    echo ============================================================
    echo.
    echo   Output: dist\ShieldHive_Server.exe
    echo.
    echo   Instructions for Judges:
    echo   1. Run ShieldHive_Server.exe
    echo   2. Open browser to http://localhost:5000
    echo   3. Connect Sentinel agents to the server
    echo   4. Session auto-expires after 60 minutes
    echo.
    echo ============================================================
) else (
    echo.
    echo [!] BUILD FAILED - Check errors above
    echo.
)

pause
