@echo off
echo ============================================
echo  Pushing to GitHub - Waga Sklepowa Projekt
echo ============================================
echo.

cd /d "%~dp0"

echo Checking git status...
git status
echo.

echo.
echo ============================================
echo  Ready to push 3 commits to GitHub:
echo ============================================
echo  1. Przygotowanie do deployment (upload + top 5)
echo  2. Fix dependencies dla Python 3.11
echo  3. Dokumentacja push help
echo ============================================
echo.

echo.
echo UWAGA: Zostaniesz poproszony o GitHub credentials
echo Username: MatyldaGrygorcewicz
echo Password: Twoj Personal Access Token (nie haslo!)
echo.
pause

echo.
echo Pushing to GitHub...
git push origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo ============================================
    echo  SUCCESS! Push completed!
    echo ============================================
    echo.
    echo Render automatycznie zacznie deployment.
    echo Sprawdz: https://dashboard.render.com
    echo.
) else (
    echo ============================================
    echo  ERROR: Push failed!
    echo ============================================
    echo.
    echo Prawdopodobnie problem z autentykacja.
    echo.
    echo ROZWIAZANIE:
    echo 1. Stworz Personal Access Token na GitHub:
    echo    https://github.com/settings/tokens
    echo 2. Wybierz: repo (full control)
    echo 3. Skopiuj token
    echo 4. Uruchom ponownie ten skrypt
    echo 5. Uzyj tokenu jako hasla
    echo.
)

pause
