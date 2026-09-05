@echo off
REM =======================================================
REM ChaskiByte Systems - Limpieza Rapida de PC de Laboratorio
REM Ejecutalo ANTES de exponer si otro grupo uso la PC antes que tu
REM =======================================================
title Limpieza de Entorno Compartido - ChaskiPC

echo =======================================================
echo   CHASKIPC - LIMPIEZA PREVENTIVA DE PUERTOS Y PROCESOS
echo =======================================================

echo [*] 1. Cerrando procesos de Java previos (evita puertos ocupados 8080, 8761, 8888)...
taskkill /F /IM java.exe /T 2>nul
taskkill /F /IM javaw.exe /T 2>nul

echo [*] 2. Deteniendo contenedores Docker que puedan estar ocupando puertos...
docker stop chaskipc-db-orden 2>nul
docker stop pagatu-prometheus-dev pagatu-grafana-dev pagatu-loki-dev pagatu-promtail-dev 2>nul

echo.
echo =======================================================
echo [LISTO] PC de laboratorio limpia y liberada.
echo Ahora puedes hacer doble clic en 'iniciar_todo.bat' sin conflictos.
echo =======================================================
pause
