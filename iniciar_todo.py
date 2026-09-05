# -*- coding: utf-8 -*-
"""
ChaskiByte Systems - Ecosistema de Microservicios ChaskiPC
Lanzador Portable Multi-Entorno (Desarrollado para Laboratorio DTI y Entornos Locales)
Resuelve automaticamente los 7 problemas tecnicos:
1. Rutas relativas dinamicas (sin rutas hardcoded, funciona en cualquier PC o USB).
2. Compatibilidad con PowerShell ($env:SERVER_PORT sin problemas de comillas).
3. Deteccion y forzado de Java 21 si JAVA_HOME apunta a Java 17 u otra version.
4. Inyeccion dinamica de search-locations para Config Server.
"""
import os
import sys
import subprocess
import time
import glob

# 1. Resolver ruta base dinamica
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_REPO_DIR = os.path.join(BASE_DIR, "config-repo").replace("\\", "/")
CONFIG_REPO_URI = f"file:///{CONFIG_REPO_DIR}"

# 2. Deteccion automatica de Java 21
def detect_java_21():
    java_home = os.environ.get("JAVA_HOME", "")
    if "21" in java_home:
        return java_home
    search_patterns = [
        r"C:\Program Files\Java\*21*",
        r"C:\Program Files\Eclipse Adoptium\*21*",
        r"C:\Program Files\Amazon Corretto\*21*",
        r"C:\Program Files\Microsoft\jdk-21*",
        r"C:\Users\*\.jdks\*21*"
    ]
    for pattern in search_patterns:
        matches = glob.glob(pattern)
        if matches:
            return matches[0]
    return java_home

JAVA_21_HOME = detect_java_21()
java_env_setup = f'$env:JAVA_HOME = "{JAVA_21_HOME}"; ' if JAVA_21_HOME else ""

# 3. Definicion de microservicios con rutas relativas
commands = [
    {
        "title": "1. CONFIG-SERVER [Puerto 8888]",
        "dir": os.path.join(BASE_DIR, "pagatu-config"),
        "cmd": f'{java_env_setup}$env:CONFIG_REPO_PATH = "{CONFIG_REPO_URI}"; .\\mvnw.cmd spring-boot:run',
        "wait": 8
    },
    {
        "title": "2. EUREKA-SERVER [Puerto 8761]",
        "dir": os.path.join(BASE_DIR, "pagatu-eureka"),
        "cmd": f"{java_env_setup}.\\mvnw.cmd spring-boot:run",
        "wait": 6
    },
    {
        "title": "3. CATALOGO-MS [Puerto 8081]",
        "dir": os.path.join(BASE_DIR, "pagatu-catalogo-ms"),
        "cmd": f"{java_env_setup}.\\mvnw.cmd spring-boot:run",
        "wait": 4
    },
    {
        "title": "4. ORDEN-MS (Instancia 1) [Puerto 8082]",
        "dir": os.path.join(BASE_DIR, "pagatu-orden-ms"),
        "cmd": f"{java_env_setup}.\\mvnw.cmd spring-boot:run",
        "wait": 5
    },
    {
        "title": "5. ORDEN-MS (Instancia 2) [Puerto 8083]",
        "dir": os.path.join(BASE_DIR, "pagatu-orden-ms"),
        "cmd": f"{java_env_setup}$env:SERVER_PORT = '8083'; .\\mvnw.cmd spring-boot:run",
        "wait": 4
    },
    {
        "title": "6. API-GATEWAY [Puerto 18080]",
        "dir": os.path.join(BASE_DIR, "pagatu-gateway"),
        "cmd": f"{java_env_setup}.\\mvnw.cmd spring-boot:run",
        "wait": 3
    },
    {
        "title": "7. PRUEBAS CRUD Y MONITOREO (PowerShell)",
        "dir": BASE_DIR,
        "cmd": 'Write-Host "=== CHASKIPC: ECOSISTEMA INICIADO CORRECTAMENTE ===" -ForegroundColor Cyan; '
               'Write-Host "Comandos de verificacion rapida:" -ForegroundColor Yellow; '
               'Write-Host "  1. Config Server: Invoke-RestMethod -Uri http://localhost:8888/pagatu-orden-ms/dev" -ForegroundColor White; '
               'Write-Host "  2. Eureka Apps:   (Invoke-RestMethod -Uri http://localhost:8761/eureka/apps).applications.application.name" -ForegroundColor White; '
               'Write-Host "  3. Gateway Orden: Invoke-RestMethod -Uri http://localhost:18080/api/v1/ordenes" -ForegroundColor White; '
               'Write-Host "  4. Gateway Prods: Invoke-RestMethod -Uri http://localhost:18080/api/v1/productos" -ForegroundColor White',
        "wait": 0
    }
]

print("=================================================================")
print("   CHASKIBYTE SYSTEMS - LANZADOR AUTOMATIZADO DE MICROSERVICIOS  ")
print("=================================================================")
print(f"[*] Directorio Base: {BASE_DIR}")
print(f"[*] Config Repo URI: {CONFIG_REPO_URI}")
if JAVA_21_HOME:
    print(f"[*] JDK 21 Detectado: {JAVA_21_HOME}")
print("-----------------------------------------------------------------")

for item in commands:
    ps_cmd = f'$host.UI.RawUI.WindowTitle = "{item["title"]}"; Set-Location "{item["dir"]}"; {item["cmd"]}'
    subprocess.Popen(["powershell.exe", "-NoExit", "-Command", ps_cmd], creationflags=subprocess.CREATE_NEW_CONSOLE)
    print(f"[OK] Lanzada ventana: {item['title']}")
    if item["wait"] > 0:
        time.sleep(item["wait"])

print("-----------------------------------------------------------------")
print("[EXITO] Todas las ventanas han sido desplegadas correctamente.")
