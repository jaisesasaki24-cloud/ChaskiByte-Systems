@echo off
REM =======================================================
REM ChaskiByte Systems - Lanzador de Observabilidad Completa
REM Levanta Prometheus (19090), Grafana (13000), Loki (13100) y Promtail
REM =======================================================
title Observabilidad ChaskiPC - Prometheus, Grafana, Loki

echo =======================================================
echo   INICIANDO STACK DE OBSERVABILIDAD CHASKIPC
echo   - Prometheus : http://localhost:19090 (Eureka Service Discovery)
echo   - Grafana    : http://localhost:13000 (User: admin / Pass: admin)
echo   - Loki       : http://localhost:13100 (Centralizador de Logs)
echo   - Promtail   : Recolector de logs desde carpeta logs/
echo =======================================================

docker info >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker no esta en ejecucion o no esta instalado.
    echo Inicia Docker Desktop antes de ejecutar este script.
    pause
    exit /b 1
)

echo [*] Levantando contenedores de observabilidad en Docker...
docker compose -f "%~dp0obs\compose-dev.yml" up -d

echo.
echo [OK] Stack de observabilidad operativo.
docker ps --filter "name=pagatu-"
echo.
echo Puedes ingresar a Grafana en: http://localhost:13000
pause
