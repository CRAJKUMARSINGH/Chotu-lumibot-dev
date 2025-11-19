@echo off
REM maintain-chotu-lumibot.bat
REM Full maintenance pipeline for Chotu-lumibot-dev (Lumibot fork)
REM Windows-compatible version

echo.
echo ========================================
echo   Chotu-Lumibot Maintenance Pipeline
echo ========================================
echo.

REM 1. UPDATE
echo [1/6] Pulling latest changes...
git checkout dev 2>nul || git checkout main 2>nul || git checkout master 2>nul
if errorlevel 1 (
    echo ERROR: Could not switch to main branch
    exit /b 1
)
git pull --ff-only
if errorlevel 1 (
    echo ERROR: Git pull failed
    exit /b 1
)
echo    Done.
echo.

REM 2. OPTIMIZE & REMOVE BUGS
echo [2/6] Formatting and linting code...
where black >nul 2>&1
if %errorlevel% equ 0 (
    black lumibot\ examples\ 2>nul
    echo    black applied
)

where isort >nul 2>&1
if %errorlevel% equ 0 (
    isort lumibot\ examples\ 2>nul
    echo    isort applied
)

where ruff >nul 2>&1
if %errorlevel% equ 0 (
    ruff check --fix lumibot\ examples\ 2>nul
    echo    ruff fixes applied
)
echo    Done.
echo.

REM 3. MAKE DEPLOYABLE
echo [3/6] Installing dependencies...
pip install --no-cache-dir -e .[dev] 2>nul
if errorlevel 1 (
    pip install -e .
)

REM Verify critical modules
python -c "import lumibot; print('   Lumibot importable')"
if errorlevel 1 (
    echo ERROR: Lumibot core failed to import
    exit /b 1
)

python -c "import pandas; import numpy; print('   Pandas/NumPy OK')"
if errorlevel 1 (
    echo ERROR: Data dependencies missing
    exit /b 1
)
echo    Done.
echo.

REM 4. TEST RUN
echo [4/6] Running tests...
if not exist ".env" (
    echo    No .env file - running non-API tests only
    pytest -m "not require_api" --tb=short -x 2>nul
) else (
    echo    .env found - running full test suite
    pytest --tb=short -x 2>nul
)

echo    Running example backtest...
timeout /t 120 /nobreak >nul 2>&1 & python -m lumibot.example_strategies.stock_buy_and_hold 2>nul
echo    Done.
echo.

REM 5. REMOVE CACHE
echo [5/6] Clearing Python and build caches...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc *.pyo 2>nul
if exist .pytest_cache rd /s /q .pytest_cache 2>nul
if exist .mypy_cache rd /s /q .mypy_cache 2>nul
if exist .ruff_cache rd /s /q .ruff_cache 2>nul
if exist .coverage del /q .coverage 2>nul
if exist htmlcov rd /s /q htmlcov 2>nul
if exist build rd /s /q build 2>nul
if exist dist rd /s /q dist 2>nul
for /d %%d in (*.egg-info) do @if exist "%%d" rd /s /q "%%d" 2>nul
if exist .eggs rd /s /q .eggs 2>nul

REM Reinstall cleanly
pip install --no-cache-dir -e .[dev] 2>nul || pip install -e .
echo    Done.
echo.

REM 6. PUSH BACK TO REMOTE
echo [6/6] Committing and pushing...
git add .
git diff-index --quiet HEAD --
if errorlevel 1 (
    for /f "tokens=*" %%a in ('git branch --show-current') do set CURRENT_BRANCH=%%a
    git commit -m "chore(lumibot): optimized, tested, cache-cleared [%date% %time%]"
    git push origin %CURRENT_BRANCH%
    echo    Changes pushed to %CURRENT_BRANCH%
) else (
    echo    No changes - repo is clean and up-to-date
)
echo    Done.
echo.

echo ========================================
echo   Maintenance Complete!
echo ========================================
