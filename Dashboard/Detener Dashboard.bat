@echo off
chcp 65001 > nul
title ErgIoT - Detener

echo ============================================================
echo   Deteniendo procesos del Dashboard
echo ============================================================
echo.

echo Matando procesos Streamlit en puerto 8501...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr "LISTENING" ^| findstr ":8501"') do (
    taskkill /PID %%a /F > nul 2>&1
    if errorlevel 0 echo   - Detenido PID %%a
)

echo Matando procesos cloudflared...
taskkill /IM cloudflared.exe /F > nul 2>&1
if errorlevel 0 echo   - cloudflared detenido

echo Cerrando ventanas con titulo "ErgIoT *"...
taskkill /FI "WINDOWTITLE eq ErgIoT *" /F > nul 2>&1

echo.
echo ============================================================
echo   Listo. Todo detenido.
echo ============================================================
timeout /t 3 > nul
