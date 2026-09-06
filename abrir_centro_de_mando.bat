@echo off
setlocal
title ChaskiPC - Centro de Mando y Sustentacion
cd /d "%~dp0"

echo ======================================================================
echo    CHASKIPC - CENTRO DE MANDO Y SUSTENTACION (EQUIPO 01)
echo    Eliceo Parillo Mostajo & Laura Vargas Cristhian Paul
echo ======================================================================
echo.

:: 1. Verificar si Python esta instalado
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [!] Python no fue detectado en PATH.
    echo [*] Intentando auto-instalacion silenciosa mediante winget...
    winget install Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements
    python --version >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo [!] No se pudo instalar Python automaticamente (posible falta de permisos).
        echo [*] Abriendo presentacion en Modo Navegador con respaldo de portapapeles...
        start "" "presentacion.html"
        exit /b 0
    )
)

:: 2. Cerrar instancias previas del servidor de control si existen en puerto 5050
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5050" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)

:: 3. Iniciar el servidor de control en segundo plano
echo [*] Iniciando Servidor de Control ChaskiPC en http://localhost:5050 ...
start /b "" python servidor_control.py

timeout /t 2 >nul

:: 4. Abrir la presentacion en el navegador
echo [*] Abriendo el Centro de Mando en tu navegador predeterminado...
start "" "http://localhost:5050"

echo.
echo ======================================================================
echo [V] CENTRO DE MANDO ACTIVO
echo [*] URL de control: http://localhost:5050
echo [*] TIP: Presiona F11 en el navegador para proyectar a pantalla completa.
echo [*] Puedes minimizar esta consola durante la sustentacion.
echo ======================================================================
pause
