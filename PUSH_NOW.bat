@echo off
cls
echo.
echo ================================================
echo    PUSH DO GITHUB - WAGA SKLEPOWA AI
echo ================================================
echo.
echo Gotowe do push:
echo   - Frontend serving (GUI bedzie dzialac!)
echo   - Upload zdjec
echo   - Top 5 wynikow
echo   - Fix dla Python 3.11
echo.
echo ================================================
echo.

cd /d "%~dp0"

git push origin main

if %ERRORLEVEL% EQU 0 (
    cls
    echo.
    echo ================================================
    echo    SUCCESS! ✓
    echo ================================================
    echo.
    echo Zmiany wypushowane na GitHub!
    echo.
    echo Render automatycznie rozpocznie deployment.
    echo Zajmie to ok. 10-15 minut.
    echo.
    echo Sprawdz status:
    echo https://dashboard.render.com
    echo.
    echo Twoja aplikacja:
    echo https://waga-sklepowa-projekt.onrender.com
    echo.
    echo ================================================
    echo.
    start https://dashboard.render.com
) else (
    echo.
    echo ================================================
    echo    Push wymaga autentykacji
    echo ================================================
    echo.
    echo Otworz GitHub Desktop i kliknij "Push origin"
    echo To najprostszy sposob!
    echo.
    echo ================================================
    echo.
)

pause
