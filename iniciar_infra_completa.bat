@echo off
REM =======================================================
REM ChaskiByte Systems - Infraestructura Completa en Docker
REM Levanta: PostgreSQL (5433) + Prometheus + Grafana + Loki
REM =======================================================
title Infraestructura Completa - PostgreSQL y Observabilidad

echo =======================================================
echo   CHASKIPC - INFRAESTRUCTURA DE DATOS Y OBSERVABILIDAD
echo =======================================================

docker info >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker Desktop no esta en ejecucion.
    echo Inicia la aplicacion Docker Desktop y vuelve a presionar una tecla.
    pause
    exit /b 1
)

echo [*] 1. Levantando PostgreSQL (puerto 5433, db: orden_db)...
docker compose -f "%~dp0infra\docker-compose-db.yml" up -d

echo [*] 2. Levantando Prometheus, Grafana, Loki y Promtail...
docker compose -f "%~dp0obs\compose-dev.yml" up -d

echo.
echo =======================================================
echo [EXITO] Toda la infraestructura esta lista:
echo   - PostgreSQL : localhost:5433 (user: admin / pass: adminpassword)
echo   - Grafana    : http://localhost:13000 (admin / admin)
echo   - Prometheus : http://localhost:19090
echo   - Loki       : http://localhost:13100
echo =======================================================
pause
