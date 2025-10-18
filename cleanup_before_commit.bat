@echo off
REM Cleanup script to remove files that shouldn't be committed
REM Run this BEFORE running create_commits.bat

echo ==========================================
echo Pre-Commit Cleanup Script
echo ==========================================
echo.

echo Step 1: Removing Python cache files...
for /d /r %%i in (__pycache__) do @if exist "%%i" rd /s /q "%%i" 2>nul
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
del /s /q *.pyd 2>nul
echo Done: Python cache cleaned
echo.

echo Step 2: Removing virtual environments...
if exist "backend\venv" rd /s /q "backend\venv" 2>nul
if exist "backend\env" rd /s /q "backend\env" 2>nul
if exist "backend\ENV" rd /s /q "backend\ENV" 2>nul
echo Done: Virtual environments removed
echo.

echo Step 3: Removing Node modules...
if exist "frontend\node_modules" rd /s /q "frontend\node_modules" 2>nul
echo Done: Node modules removed
echo.

echo Step 4: Removing build artifacts...
if exist "frontend\build" rd /s /q "frontend\build" 2>nul
if exist "backend\build" rd /s /q "backend\build" 2>nul
if exist "backend\dist" rd /s /q "backend\dist" 2>nul
echo Done: Build artifacts removed
echo.

echo Step 5: Removing logs...
if exist "logs" rd /s /q "logs" 2>nul
del /s /q *.log 2>nul
echo Done: Logs removed
echo.

echo Step 6: Removing model cache...
if exist "backend\model_cache" rd /s /q "backend\model_cache" 2>nul
echo Done: Model cache removed
echo.

echo Step 7: Removing database files...
del /s /q *.db 2>nul
del /s /q *.sqlite 2>nul
echo Done: Database files removed
echo.

echo Step 8: Removing IDE files...
if exist ".vscode" rd /s /q ".vscode" 2>nul
if exist ".idea" rd /s /q ".idea" 2>nul
del /s /q *.swp 2>nul
del /s /q *.swo 2>nul
echo Done: IDE files removed
echo.

echo Step 9: Removing OS files...
del /s /q .DS_Store 2>nul
del /s /q Thumbs.db 2>nul
echo Done: OS files removed
echo.

echo ==========================================
echo Security Checks
echo ==========================================
echo.

echo Checking for .env files...
if exist "backend\.env" (
    echo WARNING: Found backend\.env
    echo This file may contain secrets!
    echo Please review before committing.
    echo.
)

echo ==========================================
echo Cleanup Summary
echo ==========================================
echo.

echo Files that WILL be committed:
echo   - Source code (.py, .js, .jsx, .css, .html^)
echo   - Configuration (.env.example, package.json, requirements.txt^)
echo   - Documentation (.md files^)
echo   - Docker files (Dockerfile, docker-compose.yml^)
echo   - Scripts (.sh, .bat^)
echo.

echo Files that will NOT be committed (ignored^):
echo   - .env (secrets^)
echo   - venv/, node_modules/ (dependencies^)
echo   - __pycache__/ (Python cache^)
echo   - *.log (logs^)
echo   - model_cache/ (ML models^)
echo   - build/ (build artifacts^)
echo.

echo ==========================================
echo Next Steps
echo ==========================================
echo.
echo 1. Review warnings above (if any^)
echo 2. Manually check backend\.env for secrets
echo 3. Run: create_commits.bat
echo 4. Push to GitHub
echo.

if exist "backend\.env" (
    echo WARNING: backend\.env exists!
    echo.
    echo Options:
    echo   a^) If it contains REAL secrets: del backend\.env
    echo   b^) If it's just placeholders: it's safe to keep
    echo   c^) Rename: move backend\.env backend\.env.local
    echo.
)

echo Ready to commit? Run: create_commits.bat
echo.
pause
