@echo off
chcp 65001 > nul
title ErgIoT Dashboard - Lanzador

echo ============================================================
echo   ErgIoT Dashboard - PUBLICO (Internet)
echo   Universidad de La Salle ^| IoT G02 ^| 2026-1
echo ============================================================
echo.
echo  1. Lanza Streamlit en http://localhost:8501
echo  2. Lanza tunel Cloudflare con URL publica HTTPS
echo.
echo Se abriran DOS ventanas adicionales:
echo   - Una con el servidor Streamlit
echo   - Una con el tunel (alli aparecera la URL publica)
echo ============================================================
echo.

cd /d "%~dp0"

echo Iniciando Streamlit en ventana aparte...
start "ErgIoT Streamlit" cmd /k "streamlit run app.py"

echo Esperando 5 segundos a que Streamlit este listo...
timeout /t 5 /nobreak > nul

echo Iniciando tunel Cloudflare en ventana aparte...
start "ErgIoT Tunel" cmd /k "cloudflared tunnel --url http://localhost:8501"

echo.
echo ============================================================
echo  LISTO. Mira la ventana "ErgIoT Tunel" para ver la URL
echo  publica que aparece (tipo https://xxx.trycloudflare.com).
echo ============================================================
echo.
echo  Para detener todo, cierra ambas ventanas o ejecuta
echo  "Detener Dashboard.bat".
echo.
pause
