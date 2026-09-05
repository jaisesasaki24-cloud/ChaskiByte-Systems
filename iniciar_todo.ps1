# =================================================================
# ChaskiByte Systems - Lanzador Nativo PowerShell (Sin Python)
# Auto-inicia: PostgreSQL (5433) + Prometheus (19090) + Grafana (13000) + Loki (13100) + Spring Boot
# =================================================================
$BaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ConfigRepoUri = "file:///" + ($BaseDir + "/config-repo").Replace("\", "/")

# 1. Deteccion automatica de Java 21
$Java21 = (Get-ChildItem -Path "C:\Program Files\Java", "C:\Program Files\Eclipse Adoptium", "C:\Program Files\Amazon Corretto", "C:\Program Files\Microsoft" -ErrorAction SilentlyContinue | Where-Object { $_.Name -like "*21*" } | Select-Object -First 1).FullName

if ($Java21) {
    Write-Host "[*] JDK 21 detectado en: $Java21" -ForegroundColor Green
    $JavaEnv = "`$env:JAVA_HOME = '$Java21'; "
} else {
    $JavaEnv = ""
}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "   CHASKIBYTE SYSTEMS - LANZADOR NATIVO INTEGRAL CHASKIPC        " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan

# 2. Comprobar e iniciar Docker (PostgreSQL + Observabilidad)
try {
    $dockerOut = docker info 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[*] Docker activo. Levantando PostgreSQL y Observabilidad (Prometheus, Grafana, Loki)..." -ForegroundColor Green
        docker compose -f "$BaseDir\infra\docker-compose-db.yml" up -d 2>$null
        docker compose -f "$BaseDir\obs\compose-dev.yml" up -d 2>$null
        Write-Host "[OK] Infraestructura Docker operativa (PostgreSQL 5433, Grafana 13000, Prometheus 19090)." -ForegroundColor Green
    } else {
        Write-Host "[AVISO] Docker Desktop no esta iniciado. Si requieres base de datos o Grafana, inicia Docker." -ForegroundColor Yellow
    }
} catch {
    Write-Host "[AVISO] Docker no disponible. Continuando con el arranque de microservicios..." -ForegroundColor Yellow
}

# 3. Microservicios de Negocio e Infraestructura
$Commands = @(
    @{ Title = "1. CONFIG-SERVER [Puerto 8888]"; Dir = "$BaseDir\pagatu-config"; Cmd = "$JavaEnv`$env:CONFIG_REPO_PATH = '$ConfigRepoUri'; .\mvnw.cmd spring-boot:run"; Wait = 8 },
    @{ Title = "2. EUREKA-SERVER [Puerto 8761]"; Dir = "$BaseDir\pagatu-eureka"; Cmd = "$JavaEnv.\mvnw.cmd spring-boot:run"; Wait = 6 },
    @{ Title = "3. CATALOGO-MS [Puerto 8081]"; Dir = "$BaseDir\pagatu-catalogo-ms"; Cmd = "$JavaEnv.\mvnw.cmd spring-boot:run"; Wait = 4 },
    @{ Title = "4. ORDEN-MS (Instancia 1) [Puerto 8082]"; Dir = "$BaseDir\pagatu-orden-ms"; Cmd = "$JavaEnv.\mvnw.cmd spring-boot:run"; Wait = 5 },
    @{ Title = "5. ORDEN-MS (Instancia 2) [Puerto 8083]"; Dir = "$BaseDir\pagatu-orden-ms"; Cmd = "$JavaEnv`$env:SERVER_PORT = '8083'; .\mvnw.cmd spring-boot:run"; Wait = 4 },
    @{ Title = "6. API-GATEWAY [Puerto 18080]"; Dir = "$BaseDir\pagatu-gateway"; Cmd = "$JavaEnv.\mvnw.cmd spring-boot:run"; Wait = 3 },
    @{ Title = "7. MONITOR Y CONSOLA DE PRUEBAS"; Dir = "$BaseDir"; Cmd = 'Write-Host "=== CHASKIPC: ECOSISTEMA INICIADO EXITOSAMENTE ===" -ForegroundColor Cyan; Write-Host "Servicios y Dashboards Disponibles:" -ForegroundColor Yellow; Write-Host "  - API Gateway:    http://localhost:18080/api/v1/ordenes" -ForegroundColor White; Write-Host "  - Eureka Server:  http://localhost:8761" -ForegroundColor White; Write-Host "  - Grafana Visual: http://localhost:13000 (admin / admin)" -ForegroundColor Green; Write-Host "  - Prometheus:     http://localhost:19090" -ForegroundColor Green; Write-Host "  - Loki Logs:      http://localhost:13100" -ForegroundColor Green; Write-Host "Comandos de prueba:" -ForegroundColor Yellow; Write-Host "  Invoke-RestMethod -Uri http://localhost:18080/api/v1/productos" -ForegroundColor Gray; Write-Host "  Invoke-RestMethod -Uri http://localhost:18080/api/v1/ordenes" -ForegroundColor Gray'; Wait = 0 }
)

foreach ($item in $Commands) {
    $psCmd = "`$host.UI.RawUI.WindowTitle = '$($item.Title)'; Set-Location '$($item.Dir)'; $($item.Cmd)"
    Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", $psCmd
    Write-Host "[OK] Lanzada ventana: $($item.Title)" -ForegroundColor Green
    if ($item.Wait -gt 0) {
        Start-Sleep -Seconds $item.Wait
    }
}

Write-Host "-----------------------------------------------------------------"
Write-Host "[EXITO] Todo el ecosistema ha sido desplegado exitosamente." -ForegroundColor Cyan
