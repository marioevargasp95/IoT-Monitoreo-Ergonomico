@echo off
chcp 65001 > nul
title ErgIoT Dashboard - Local

echo ============================================================
echo   ErgIoT Dashboard - Monitoreo Ergonomico
echo   Universidad de La Salle ^| IoT G02 ^| 2026-1
echo ============================================================
echo.
echo Iniciando Streamlit en http://localhost:8501
echo.
echo Cierra esta ventana cuando termines (Ctrl+C o boton X).
echo ============================================================
echo.

cd /d "%~dp0"
streamlit run app.py

echo.
echo Dashboard detenido. Presiona cualquier tecla para cerrar.
pause > nul
