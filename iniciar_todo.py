# -*- coding: utf-8 -*-
# Iniciar todo el ecosistema en ventanas visibles de PowerShell
import subprocess, time

commands = [
    {
        "title": "1. CONFIG-SERVER [Puerto 8888]",
        "dir": r"C:\Users\USUARIO\Documents\Tarea Eureka\pagatu-config",
        "cmd": r".\mvnw.cmd spring-boot:run",
        "wait": 8
    },
    {
        "title": "2. EUREKA-SERVER [Puerto 8761]",
        "dir": r"C:\Users\USUARIO\Documents\Tarea Eureka\pagatu-eureka",
        "cmd": r".\mvnw.cmd spring-boot:run",
        "wait": 6
    },
    {
        "title": "3. CATALOGO-MS [Puerto 8081]",
        "dir": r"C:\Users\USUARIO\Documents\Tarea Eureka\pagatu-catalogo-ms",
        "cmd": r".\mvnw.cmd spring-boot:run",
        "wait": 4
    },
    {
        "title": "4. ORDEN-MS (Instancia 1) [Puerto 8082]",
        "dir": r"C:\Users\USUARIO\Documents\Tarea Eureka\pagatu-orden-ms",
        "cmd": r".\mvnw.cmd spring-boot:run",
        "wait": 5
    },
    {
        "title": "5. ORDEN-MS (Instancia 2) [Puerto 8083]",
        "dir": r"C:\Users\USUARIO\Documents\Tarea Eureka\pagatu-orden-ms",
        "cmd": r'.\mvnw.cmd spring-boot:run -Dspring-boot.run.arguments="--server.port=8083"',
        "wait": 4
    },
    {
        "title": "6. API-GATEWAY [Puerto 18080]",
        "dir": r"C:\Users\USUARIO\Documents\Tarea Eureka\pagatu-gateway",
        "cmd": r".\mvnw.cmd spring-boot:run",
        "wait": 3
    },
    {
        "title": "7. PRUEBAS CRUD Y COMANDOS (PowerShell)",
        "dir": r"C:\Users\USUARIO\Documents\Tarea Eureka",
        "cmd": r'Write-Host "=== VENTANA LISTA PARA TUS PRUEBAS CRUD Y CAPTURAS ===" -ForegroundColor Cyan; Write-Host "Ejecuta aqui tus comandos de prueba:" -ForegroundColor Yellow; Write-Host "Invoke-RestMethod -Uri http://localhost:8888/pagatu-orden-ms/dev" -ForegroundColor Green; Write-Host "(Invoke-RestMethod -Uri http://localhost:8761/eureka/apps).applications.application.name" -ForegroundColor Green; Write-Host "Invoke-RestMethod -Uri http://localhost:18080/api/ordenes" -ForegroundColor Green',
        "wait": 0
    }
]

for item in commands:
    ps_cmd = f'$host.UI.RawUI.WindowTitle = "{item["title"]}"; Set-Location "{item["dir"]}"; {item["cmd"]}'
    # Start separate visible PowerShell window
    subprocess.Popen(["powershell.exe", "-NoExit", "-Command", ps_cmd], creationflags=subprocess.CREATE_NEW_CONSOLE)
    print(f"Lanzada ventana: {item['title']}")
    if item["wait"] > 0:
        time.sleep(item["wait"])

print("Todas las ventanas han sido abiertas exitosamente en tu escritorio.")
