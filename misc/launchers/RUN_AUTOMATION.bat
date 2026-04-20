@echo off
echo ============================================================
echo   CONTENT AUTOMATION AI - LAUNCHER
echo ============================================================
echo.

REM Check if OPENAI_API_KEY is set
if not defined OPENAI_API_KEY (
    echo [WARNING] OPENAI_API_KEY is not set.
    echo.
    echo To set it for this session:
    echo   set OPENAI_API_KEY=your-api-key-here
    echo.
    echo Or permanently in PowerShell:
    echo   [System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'your-key', 'User'^)
    echo.
    echo The system will run in demo mode without actual content generation.
    echo.
    pause
)

echo.
echo ============================================================
echo   MENU - Select an option:
echo ============================================================
echo.
echo   1. Run system test
echo   2. Generate video batch (requires API key)
echo   3. View statistics
echo   4. Add monetization hooks
echo   5. Schedule batch for publishing
echo   6. View help / documentation
echo   7. Exit
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto test
if "%choice%"=="2" goto generate
if "%choice%"=="3" goto stats
if "%choice%"=="4" goto monetize
if "%choice%"=="5" goto schedule
if "%choice%"=="6" goto help
if "%choice%"=="7" goto exit

echo Invalid choice. Please try again.
pause
goto menu

:test
echo.
echo Running system test...
.venv\Scripts\python.exe simple_test.py
pause
goto menu

:generate
echo.
echo ============================================================
echo   GENERATE VIDEO BATCH
echo ============================================================
echo.
set /p topic="Enter topic (e.g., 'relationship psychology facts'): "
set /p count="Enter number of videos (default 5): "
set /p batch="Enter batch name (default: auto-generated): "

if "%count%"=="" set count=5

if "%batch%"=="" (
    .venv\Scripts\python.exe content_production_pipeline.py --topic "%topic%" --count %count%
) else (
    .venv\Scripts\python.exe content_production_pipeline.py --topic "%topic%" --count %count% --batch-name %batch%
)

echo.
echo Batch generation complete!
pause
goto menu

:stats
echo.
echo ============================================================
echo   STATISTICS
echo ============================================================
echo.
.venv\Scripts\python.exe content_production_pipeline.py --stats
pause
goto menu

:monetize
echo.
echo ============================================================
echo   ADD MONETIZATION HOOKS
echo ============================================================
echo.
set /p batch="Enter batch name: "
set /p cta="Enter CTA text (e.g., 'Try LoveGuard Premium!'): "

.venv\Scripts\python.exe content_production_pipeline.py --batch %batch% --add-cta "%cta%"

echo.
echo Monetization hooks added!
pause
goto menu

:schedule
echo.
echo ============================================================
echo   SCHEDULE BATCH FOR PUBLISHING
echo ============================================================
echo.
set /p batch="Enter batch name: "
set /p interval="Enter interval (daily/weekly, default: daily): "

if "%interval%"=="" set interval=daily

.venv\Scripts\python.exe content_production_pipeline.py --batch %batch% --schedule --interval %interval%

echo.
echo Batch scheduled!
pause
goto menu

:help
echo.
echo ============================================================
echo   DOCUMENTATION
echo ============================================================
echo.
echo Available documentation files:
echo   - 00_START_HERE.md - Quick start guide
echo   - GROWTH_SYSTEM_README.md - Complete system overview
echo   - QUICK_REFERENCE.md - Command reference
echo   - SOCIAL_MEDIA_GROWTH_GUIDE.md - Growth strategies
echo.
echo For PowerShell helpers:
echo   . .\social_media_helpers.ps1
echo.
pause
goto menu

:exit
echo.
echo Thank you for using Content Automation AI!
echo.
exit /b 0
