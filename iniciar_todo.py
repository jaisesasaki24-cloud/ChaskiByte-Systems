# -*- coding: utf-8 -*-
"""
ChaskiByte Systems - Ecosistema de Microservicios ChaskiPC
Lanzador Automatizado Integral:
1. Docker Infra: Levanta automáticamente PostgreSQL (5433), Prometheus (19090), Grafana (13000), Loki (13100) si Docker está activo.
2. Rutas Relativas Dinámicas: 100% portable a cualquier PC, laboratorio o unidad USB.
3. Detección Inteligente de Java 21: Evita conflictos de versiones con JDKs previos.
4. Microservicios Spring Boot: Config Server, Eureka, Catalogo, Orden (2 instancias) y Gateway en ventanas independientes.
"""
import os
import sys
import subprocess
import time
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_REPO_DIR = os.path.join(BASE_DIR, "config-repo").replace("\\", "/")
CONFIG_REPO_URI = f"file:///{CONFIG_REPO_DIR}"

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

print("=================================================================")
print("   CHASKIBYTE SYSTEMS - LANZADOR AUTOMATIZADO INTEGRAL          ")
print("=================================================================")
print(f"[*] Directorio Base: {BASE_DIR}")
print(f"[*] Config Repo URI: {CONFIG_REPO_URI}")
if JAVA_21_HOME:
    print(f"[*] JDK 21 Detectado: {JAVA_21_HOME}")
print("-----------------------------------------------------------------")

# Comprobar e iniciar Docker (PostgreSQL + Observabilidad)
try:
    res = subprocess.run(["docker", "info"], capture_output=True, text=True, timeout=4)
    if res.returncode == 0:
        print("[*] Docker detectado. Levantando PostgreSQL y Stack de Observabilidad...")
        subprocess.run(["docker", "compose", "-f", os.path.join(BASE_DIR, "infra", "docker-compose-db.yml"), "up", "-d"], capture_output=True)
        subprocess.run(["docker", "compose", "-f", os.path.join(BASE_DIR, "obs", "compose-dev.yml"), "up", "-d"], capture_output=True)
        print("[OK] PostgreSQL (5433), Prometheus (19090), Grafana (13000), Loki (13100) listos.")
    else:
        print("[AVISO] Docker Desktop no esta iniciado. Si requieres base de datos o Grafana, inicia Docker.")
except Exception:
    print("[AVISO] Docker no disponible. Continuando con arranque de microservicios...")

print("-----------------------------------------------------------------")

commands = [
    {
        "title": "1. CONFIG-SERVER [Puerto 8888]",
        "dir": os.path.join(BASE_DIR, "infra", "pagatu-config"),
        "cmd": f'{java_env_setup}$env:CONFIG_REPO_PATH = "{CONFIG_REPO_URI}"; .\\mvnw.cmd spring-boot:run',
        "wait": 8
    },
    {
        "title": "2. EUREKA-SERVER [Puerto 8761]",
        "dir": os.path.join(BASE_DIR, "infra", "pagatu-eureka"),
        "cmd": f"{java_env_setup}.\\mvnw.cmd spring-boot:run",
        "wait": 6
    },
    {
        "title": "3. CATALOGO-MS [Puerto 8081]",
        "dir": os.path.join(BASE_DIR, "services", "pagatu-catalogo-ms"),
        "cmd": f"{java_env_setup}.\\mvnw.cmd spring-boot:run",
        "wait": 4
    },
    {
        "title": "4. ORDEN-MS (Instancia 1) [Puerto 8082]",
        "dir": os.path.join(BASE_DIR, "services", "pagatu-orden-ms"),
        "cmd": f"{java_env_setup}.\\mvnw.cmd spring-boot:run",
        "wait": 5
    },
    {
        "title": "5. ORDEN-MS (Instancia 2) [Puerto 8083]",
        "dir": os.path.join(BASE_DIR, "services", "pagatu-orden-ms"),
        "cmd": f"{java_env_setup}$env:SERVER_PORT = '8083'; .\\mvnw.cmd spring-boot:run",
        "wait": 4
    },
    {
        "title": "6. API-GATEWAY [Puerto 18080]",
        "dir": os.path.join(BASE_DIR, "infra", "pagatu-gateway"),
        "cmd": f"{java_env_setup}.\\mvnw.cmd spring-boot:run",
        "wait": 3
    },
    {
        "title": "7. MONITOR Y CONSOLA DE PRUEBAS",
        "dir": BASE_DIR,
        "cmd": 'Write-Host "=== CHASKIPC: ECOSISTEMA INICIADO CORRECTAMENTE ===" -ForegroundColor Cyan; '
               'Write-Host "Enlaces y Servicios Disponibles:" -ForegroundColor Yellow; '
               'Write-Host "  - API Gateway:    http://localhost:18080/api/v1/ordenes" -ForegroundColor White; '
               'Write-Host "  - Eureka Server:  http://localhost:8761" -ForegroundColor White; '
               'Write-Host "  - Config Server:  http://localhost:8888/pagatu-orden-ms/dev" -ForegroundColor White; '
               'Write-Host "  - Grafana Visual: http://localhost:13000 (admin / admin)" -ForegroundColor Green; '
               'Write-Host "  - Prometheus:     http://localhost:19090" -ForegroundColor Green; '
               'Write-Host "  - Loki Logs:      http://localhost:13100" -ForegroundColor Green; '
               'Write-Host "Comandos de prueba rapida:" -ForegroundColor Yellow; '
               'Write-Host "  Invoke-RestMethod -Uri http://localhost:18080/api/v1/productos" -ForegroundColor Gray; '
               'Write-Host "  Invoke-RestMethod -Uri http://localhost:18080/api/v1/ordenes" -ForegroundColor Gray',
        "wait": 0
    }
]

for item in commands:
    ps_cmd = f'$host.UI.RawUI.WindowTitle = "{item["title"]}"; Set-Location "{item["dir"]}"; {item["cmd"]}'
    subprocess.Popen(["powershell.exe", "-NoExit", "-Command", ps_cmd], creationflags=subprocess.CREATE_NEW_CONSOLE)
    print(f"[OK] Lanzada ventana: {item['title']}")
    if item["wait"] > 0:
        time.sleep(item["wait"])

print("-----------------------------------------------------------------")
print("[EXITO] Ecosistema completo desplegado exitosamente.")
