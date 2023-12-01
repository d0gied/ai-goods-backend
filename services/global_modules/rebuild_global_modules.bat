@echo off
setlocal

echo Rebuilding global modules...

:: check if poetry is installed
where /q poetry
if errorlevel 1 (
    echo Poetry could not be found
    exit /b
)

:: get current version from poetry
for /f "tokens=2" %%i in ('poetry version') do set POETRY_VERSION=%%i

:: Print current version
echo Current version is %POETRY_VERSION%

:: ask new version
set /p NEW_VERSION=Enter new version: 

:: Print new version
echo New version is %NEW_VERSION%

:: check if new version is valid
echo %NEW_VERSION%| findstr /r "^[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\(\.[0-9][0-9]*\)\?$" >nul
if errorlevel 1 (
    echo New version is not valid
    exit /b
)

:: check if new version is greater than current version
for /f "tokens=1 delims=." %%i in ("%NEW_VERSION%") do set NEW_MAJOR=%%i
for /f "tokens=1 delims=." %%i in ("%POETRY_VERSION%") do set CURRENT_MAJOR=%%i
if %NEW_MAJOR% lss %CURRENT_MAJOR% (
    echo New version is not greater than current version
    exit /b
)

poetry version %NEW_VERSION%

:: for all services in parent directory do poetry update
for /d %%d in (../*/) do (
    echo Updating %%d
    cd %%d
    poetry update global_modules
)

cd ../global_modules

echo Done!