@echo off
REM Script para arrancar la base de datos PostgreSQL de ChaskiPC
REM Resuelve Connection refused: localhost:5433 y password authentication
title Iniciar Base de Datos PostgreSQL - ChaskiPC

echo =======================================================
echo    INICIANDO POSTGRESQL PARA CHASKIPC (PUERTO 5433)
echo =======================================================

docker info >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker no esta en ejecucion o no esta instalado.
    echo Asegurate de abrir Docker Desktop antes de ejecutar este script.
    pause
    exit /b 1
)

echo [*] Levantando contenedor chaskipc-db-orden con credenciales admin/adminpassword...
docker compose -f "%~dp0infra\docker-compose-db.yml" up -d

echo.
echo [OK] Base de datos lista en localhost:5433 (orden_db)
docker ps --filter "name=chaskipc-db-orden"
pause
