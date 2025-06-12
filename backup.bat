@echo off
setlocal

rem -------------------------------------------------------------
rem Set required environment variables for Restic
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
rem interval is 36 hours in seconds
set /a INTERVAL=129600

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
rem 5. Decide: run or skip
rem -------------------------------------------------------------
if %DIFF% GEQ %INTERVAL% (
    echo This window will close automatically once the backup is complete.
    echo.
    restic --verbose backup "%USERPROFILE%\Desktop" "%USERPROFILE%\Downloads"
    if errorlevel 1 (
        echo Backup failed.
        exit /b 1
    )
    restic --verbose forget --keep-within 3m
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
