# =================================================================
# ChaskiByte Systems - Lanzador Nativo PowerShell (Sin Python)
# Solucion al Problema #2 (Falta de Python en PCs de Laboratorio)
# =================================================================
$BaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ConfigRepoUri = "file:///" + ($BaseDir + "/config-repo").Replace("\", "/")

# Deteccion automatica de Java 21
$Java21 = (Get-ChildItem -Path "C:\Program Files\Java", "C:\Program Files\Eclipse Adoptium", "C:\Program Files\Amazon Corretto", "C:\Program Files\Microsoft" -ErrorAction SilentlyContinue | Where-Object { $_.Name -like "*21*" } | Select-Object -First 1).FullName

if ($Java21) {
    Write-Host "[*] JDK 21 detectado en: $Java21" -ForegroundColor Green
    $JavaEnv = "`$env:JAVA_HOME = '$Java21'; "
} else {
    $JavaEnv = ""
}

$Commands = @(
    @{ Title = "1. CONFIG-SERVER [Puerto 8888]"; Dir = "$BaseDir\pagatu-config"; Cmd = "$JavaEnv`$env:CONFIG_REPO_PATH = '$ConfigRepoUri'; .\mvnw.cmd spring-boot:run"; Wait = 8 },
    @{ Title = "2. EUREKA-SERVER [Puerto 8761]"; Dir = "$BaseDir\pagatu-eureka"; Cmd = "$JavaEnv.\mvnw.cmd spring-boot:run"; Wait = 6 },
    @{ Title = "3. CATALOGO-MS [Puerto 8081]"; Dir = "$BaseDir\pagatu-catalogo-ms"; Cmd = "$JavaEnv.\mvnw.cmd spring-boot:run"; Wait = 4 },
    @{ Title = "4. ORDEN-MS (Instancia 1) [Puerto 8082]"; Dir = "$BaseDir\pagatu-orden-ms"; Cmd = "$JavaEnv.\mvnw.cmd spring-boot:run"; Wait = 5 },
    @{ Title = "5. ORDEN-MS (Instancia 2) [Puerto 8083]"; Dir = "$BaseDir\pagatu-orden-ms"; Cmd = "$JavaEnv`$env:SERVER_PORT = '8083'; .\mvnw.cmd spring-boot:run"; Wait = 4 },
    @{ Title = "6. API-GATEWAY [Puerto 18080]"; Dir = "$BaseDir\pagatu-gateway"; Cmd = "$JavaEnv.\mvnw.cmd spring-boot:run"; Wait = 3 },
    @{ Title = "7. PRUEBAS CRUD Y MONITOREO"; Dir = "$BaseDir"; Cmd = 'Write-Host "=== CHASKIPC: ECOSISTEMA INICIADO EXITOSAMENTE ===" -ForegroundColor Cyan; Write-Host "Comandos de verificacion:" -ForegroundColor Yellow; Write-Host "  Invoke-RestMethod -Uri http://localhost:8888/pagatu-orden-ms/dev" -ForegroundColor White; Write-Host "  (Invoke-RestMethod -Uri http://localhost:8761/eureka/apps).applications.application.name" -ForegroundColor White; Write-Host "  Invoke-RestMethod -Uri http://localhost:18080/api/v1/ordenes" -ForegroundColor White'; Wait = 0 }
)

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "   CHASKIBYTE SYSTEMS - LANZADOR NATIVO POWERSHELL CHASKIPC      " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan

foreach ($item in $Commands) {
    $psCmd = "`$host.UI.RawUI.WindowTitle = '$($item.Title)'; Set-Location '$($item.Dir)'; $($item.Cmd)"
    Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", $psCmd
    Write-Host "[OK] Lanzada ventana: $($item.Title)" -ForegroundColor Green
    if ($item.Wait -gt 0) {
        Start-Sleep -Seconds $item.Wait
    }
}

Write-Host "-----------------------------------------------------------------"
Write-Host "[EXITO] Microservicios desplegados en ventanas independientes." -ForegroundColor Cyan
