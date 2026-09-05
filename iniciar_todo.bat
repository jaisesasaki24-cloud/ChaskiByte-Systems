@echo off
REM =================================================================
REM ChaskiByte Systems - Lanzador Universal (.bat)
REM Detecta automaticamente si Python esta instalado o usa PowerShell
REM =================================================================
title Lanzador ChaskiByte Systems

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Python detectado. Ejecutando iniciar_todo.py...
    python "%~dp0iniciar_todo.py"
) else (
    echo [INFO] Python no encontrado en PATH. Ejecutando lanzador nativo PowerShell...
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0iniciar_todo.ps1"
)

pause
