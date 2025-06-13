@echo off
setlocal

rem -------------------------------------------------------------
rem Set required environment variables for S3 and Restic
rem -------------------------------------------------------------
set "AWS_ACCESS_KEY_ID=%1"
set "AWS_SECRET_ACCESS_KEY=%2"
set "RESTIC_REPOSITORY=%3"
set "RESTIC_PASSWORD=%4"

rem -------------------------------------------------------------
rem 1. Configuration
rem -------------------------------------------------------------

set "SCRIPT_DIR=%~dp0"
set "LAST_RUN_FILE=%SCRIPT_DIR%last_run.txt"
set /a INTERVAL=%5

rem -------------------------------------------------------------
rem 2. Get current time in seconds since epoch
rem Requires PowerShell
rem -------------------------------------------------------------
for /f %%A in ('powershell -NoProfile -Command "[int](Get-Date -UFormat %%s)"') do set NOW=%%A

rem -------------------------------------------------------------
rem 3. Read last run time (default to 0)
rem -------------------------------------------------------------
set "LAST_RUN=0"
if exist "%LAST_RUN_FILE%" (
    set /p LAST_RUN=<"%LAST_RUN_FILE%"
)

rem -------------------------------------------------------------
rem 4. Calculate time difference
rem -------------------------------------------------------------
set /a DIFF=%NOW% - %LAST_RUN%
if %DIFF% LSS 0 (
    set /a DIFF=%INTERVAL% + 1
)

rem -------------------------------------------------------------
rem 5. Collect backup paths from argument 5 onwards
rem -------------------------------------------------------------
set "BACKUP_PATHS="
setlocal enabledelayedexpansion
set i=6
:collect_paths
call set "arg=%%%i%%"
if defined arg (
    set "BACKUP_PATHS=!BACKUP_PATHS! "!arg!""
    set /a i+=1
    goto collect_paths
)
endlocal & set "BACKUP_PATHS=%BACKUP_PATHS%"

rem -------------------------------------------------------------
rem 6. Decide: run or skip
rem -------------------------------------------------------------
if %DIFF% GEQ %INTERVAL% (
    echo This window will close automatically once the backup is complete.
    echo.
    restic --verbose backup %BACKUP_PATHS%
    if errorlevel 1 (
        echo Backup failed.
        exit /b 1
    )
    restic forget --group-by paths --keep-within 7d --keep-last 10 --prune
    if errorlevel 1 (
        echo Forget failed.
        exit /b 1
    )
    echo Backup completed successfully.
    echo %NOW% > "%LAST_RUN_FILE%"
) else (
    echo Backup skipped - only %DIFF% seconds since last run.
)

endlocal
