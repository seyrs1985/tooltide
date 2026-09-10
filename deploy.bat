@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title ToolTide - Deploy

rem WARNING: never paste your real token into this file! It gets committed to
rem git and pushed to GitHub = leaked. This script reads it from git config
rem instead (saved automatically on your first run below, or set with:
rem   git config --global tooltide.token github_pat_xxx )

rem ---- locate Git Bash ----------------------------------------------------
set "BASH="
if exist "%ProgramFiles%\Git\bin\bash.exe" set "BASH=%ProgramFiles%\Git\bin\bash.exe"
if exist "I:\Program Files\Git\bin\bash.exe" set "BASH=I:\Program Files\Git\bin\bash.exe"
if not defined BASH (
  for /f "delims=" %%i in ('where bash 2^>nul') do if not defined BASH set "BASH=%%i"
)
if not defined BASH (
  echo [X] Git Bash not found. Please install "Git for Windows" first.
  pause
  exit /b 1
)

set "GITX=%BASH:bin\bash.exe=cmd\git.exe%"
if not exist "%GITX%" (
  for /f "delims=" %%i in ('where git 2^>nul') do set "GITX=%%i"
)

echo ==========================================================
echo   ToolTide one-click deploy
echo   Site: https://seyrs1985.github.io/tooltide/
echo ==========================================================
echo.

rem ---- step 1: token (saved to LOCAL git config, never to files/git) ------
set "TOKEN="
set /p TOKEN=Step 1/2 - Paste GitHub token then Enter (leave empty if saved before):
if defined TOKEN (
  "%GITX%" config --global tooltide.token "%TOKEN%"
  if errorlevel 1 (
    echo [X] Failed to save token.
    pause
    exit /b 1
  )
  echo     Token saved to local git config. It never leaves this PC.
) else (
  "%GITX%" config --get tooltide.token >nul 2>nul
  if errorlevel 1 (
    echo [X] No token found. Get one at: https://github.com/settings/personal-access-tokens/new
    echo     Permissions: Contents RW + Administration RW, resource owner = seyrs1985.
    pause
    exit /b 2
  )
  echo     Using saved token.
)
echo.

rem ---- step 2: deploy -----------------------------------------------------
echo Step 2/2 - Building and deploying...
echo ----------------------------------------------------------
"%BASH%" -lc "cd ""$(cygpath -u '%~dp0')"" && bash engine/deploy.sh"
set "RC=%errorlevel%"
echo ----------------------------------------------------------
if "%RC%"=="0" (
  echo [OK] Deploy finished.
) else (
  echo [!] Deploy exited with code %RC%. If it says "token missing", redo step 1.
)
pause
