@echo off
REM False Positive Rate Testing Script (Windows)
REM Runs FPR tests inside Docker container

echo ========================================
echo False Positive Rate (FPR) Testing Suite
echo ========================================
echo.

REM Check if container is running
docker ps | findstr moderation_backend >nul 2>&1
if errorlevel 1 (
    echo ERROR: moderation_backend container is not running
    echo Please start the backend with: docker-compose up -d
    exit /b 1
)

echo Running FPR tests in Docker container...
echo.

REM Run the FPR test script
docker exec moderation_backend python scripts/run_fpr_tests.py %*

echo.
echo ========================================
echo FPR Testing Complete
echo ========================================
echo.
echo Results saved to backend/test_results/
echo.

pause
