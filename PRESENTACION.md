# 🖥️ Presentación Oficial de Sustentación - Unidad I
## Sistema Distribuido Base: ChaskiPC Hardware E-Commerce
**Equipo:** Equipo 01 / Grupo 4 - ChaskiByte Systems  
**Estudiante:** Eliceo Parillo Mostajo  
**Docente:** Ing. Abel Ángel Sullón Macalupu  
**Curso:** Desarrollo de Aplicaciones Distribuidas  

---

## 📑 Diapositiva 1: Portada y Proyecto Sello
* **Nombre del Proyecto:** ChaskiPC - E-Commerce Distribuido de Computadoras y Hardware de Alta Gama.
* **Integrantes y Roles:**
  * **Eliceo Parillo Mostajo:** Arquitectura Backend, Microservicio Transaccional (`pc-orden-ms`), Microservicio No Transaccional (`pc-catalogo-ms`), Config Server, Eureka Server, Gateway y Observabilidad.
  * **Laura Vargas Cristhian Paul:** Pasarela de Pagos (Mercado Pago) y Seguridad JWT.
* **Objetivo:** Demostrar una arquitectura distribuida tolerante a fallos, balanceada, configurable y observable lista para producción.

---

## 📑 Diapositiva 2: Punto 2.4 - Arquitectura del Sistema Distribuido Base
* **Punto Único de Acceso:** API Gateway Reactivo (`pagatu-gateway`) en puerto **18080** (DEV) / **28080** (PROD).
* **Service Registry & Discovery:** Netflix Eureka (`pagatu-eureka`) en puerto **8761**.
* **Configuración Centralizada:** Spring Cloud Config Server (`pagatu-config`) en puerto **8888** conectado a `config-repo`.
* **Microservicios de Negocio:**
  * `pc-catalogo-ms`: Catálogo de hardware (Puerto **8081**).
  * `pc-orden-ms` (Instancia 1): Gestión de compras y facturación (Puerto **8082**).
  * `pc-orden-ms` (Instancia 2): Réplica concurrente (Puerto **8083**).
* **Persistencia:** PostgreSQL en contenedor Docker (`chaskipc-db-orden` puerto **5433**).
* **Observabilidad Integral:** Prometheus (19090) con auto-discovery vía Eureka + Grafana (13000) con dashboards automáticos + Loki (13100) y Promtail.

---

## 📑 Diapositiva 3: Punto 2.1 y 2.2 - Alcance de Servicios y Contrato REST
### 1. Catálogo de Hardware (`pc-catalogo-ms` - No Transaccional)
* Entidades JPA: `Categoria` y `Producto` (CPUs Ryzen, GPUs RTX, Memorias DDR5, SSDs NVMe).
* Endpoints expuestos por el Gateway:
  * `GET /api/v1/categorias`: Listado de categorías.
  * `GET /api/v1/productos`: Catálogo general con stock y especificaciones técnicas.
  * `GET /api/v1/productos?categoriaId=1`: Filtro dinámico por componente.
  * `POST /api/v1/productos`: Alta de nuevos componentes de cómputo.

### 2. Órdenes y Facturación (`pc-orden-ms` - Transaccional)
* Estructura Cabecera-Detalle: `Orden` y `DetalleOrden`.
* Lógica fiscal peruana: Cálculo automático de Subtotal e IGV del 18%.
* Endpoints expuestos por el Gateway:
  * `GET /api/v1/ordenes`: Lista histórica de compras.
  * `GET /api/v1/ordenes/{id}`: Consulta con desglose de ítems e impuestos.
  * `POST /api/v1/ordenes`: Creación de orden (`BOLETA_SIMPLE`, `BOLETA_CON_DNI`, `FACTURA`).
  * Códigos HTTP estandarizados: `200 OK`, `201 Created`, `400 Bad Request`, `404 Not Found`.

---

## 📑 Diapositiva 4: Punto 2.3 - Configuración Externalizada (DEV vs PROD)
* **Cumplimiento del Factor III (Twelve-Factor App):** Cero configuraciones quemadas en código fuente.
* **Entorno DEV (`*-dev.yml`):**
  * PostgreSQL en `localhost:5433` con DDL `update`.
  * Logs en nivel `DEBUG`.
  * Exposición total de Actuator (`health,info,metrics,prometheus`).
* **Entorno PROD (`*-prod.yml`):**
  * Red interna Docker aislada `pagatu-prod-net`.
  * Credenciales inyectadas por variables de entorno seguras.
  * Hibernate DDL `validate` para máxima protección de integridad.

---

## 📑 Diapositiva 5: Punto 4 - Secuencia de Sustentación en Vivo (7 Pasos)

### 🚀 Enlaces Directos en Vivo:
* **Eureka Dashboard:** [http://localhost:8761](http://localhost:8761)
* **API Gateway (Órdenes):** [http://localhost:18080/api/v1/ordenes](http://localhost:18080/api/v1/ordenes)
* **API Gateway (Productos):** [http://localhost:18080/api/v1/productos](http://localhost:18080/api/v1/productos)
* **Config Server DEV:** [http://localhost:8888/pagatu-orden-ms/dev](http://localhost:8888/pagatu-orden-ms/dev)
* **Grafana Dashboard:** [http://localhost:13000](http://localhost:13000) (admin / admin)
* **Prometheus Targets:** [http://localhost:19090/targets](http://localhost:19090/targets)

### 📋 Comandos de Prueba para PowerShell:

#### 1. Caso Éxito (201 Created) - Crear Orden con 18% IGV:
```powershell
$orden = @{
    cliente = "Eliceo Parillo Mostajo"
    tipoComprobante = "FACTURA"
    metodoPago = "MERCADO_PAGO"
    detalles = @(
        @{ productoId = 1; nombreProducto = "AMD Ryzen 7 7800X3D"; precioUnitario = 1780.00; cantidad = 1 },
        @{ productoId = 4; nombreProducto = "Kingston Fury 1TB NVMe Gen4"; precioUnitario = 380.00; cantidad = 1 }
    )
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Post -Uri "http://localhost:18080/api/v1/ordenes" -Body $orden -ContentType "application/json"
```

#### 2. Caso Validación Fallida (400 Bad Request):
```powershell
try {
    Invoke-RestMethod -Method Post -Uri "http://localhost:18080/api/v1/ordenes" -Body "{}" -ContentType "application/json"
} catch {
    Write-Host "Código HTTP capturado:" $_.Exception.Response.StatusCode.value__ -ForegroundColor Red
}
```

#### 3. Caso Recurso Inexistente (404 Not Found):
```powershell
try {
    Invoke-RestMethod -Uri "http://localhost:18080/api/v1/ordenes/99999"
} catch {
    Write-Host "Código HTTP capturado:" $_.Exception.Response.StatusCode.value__ -ForegroundColor Yellow
}
```

#### 4. Prueba de Balanceo Round-Robin (4 Peticiones al Gateway):
```powershell
Write-Host "Disparando 4 peticiones al Gateway (revisa consolas 8082 y 8083)..." -ForegroundColor Cyan
1..4 | ForEach-Object {
    $r = Invoke-RestMethod -Uri "http://localhost:18080/api/v1/ordenes"
    Write-Host "Petición $_ procesada con éxito por una réplica." -ForegroundColor Green
    Start-Sleep -Milliseconds 400
}
```

#### 5. Prueba de Tolerancia a Fallos:
```powershell
# Apaga la consola de la instancia 8082 y ejecuta:
Invoke-RestMethod -Uri "http://localhost:18080/api/v1/ordenes"
# El Gateway responderá inmediatamente desde la 8083 sin error.
```


---

## 📑 Diapositiva 6: Desafíos DevOps Superados en Laboratorio DTI
* **7 Desafíos Técnicos de Portabilidad Resueltos:**
  1. Rutas relativas automáticas en vez de hardcoded.
  2. Lanzador nativo `iniciar_todo.ps1` que no depende de Python.
  3. Detección forzada de JDK 21 contra conflictos con Java 17.
  4. Sintaxis `$env:SERVER_PORT` en PowerShell evitando errores de comillas.
  5. Fallback dinámico `${CONFIG_REPO_PATH}` en Config Server.
  6. Script `iniciar_db.bat` con PostgreSQL en puerto 5433.
  7. Estandarización de usuario `admin` y clave `adminpassword`.

---

## 📑 Diapositiva 7: Punto 3 - Respuestas Clave del Balotario Teórico
* **P1: Puerto no fijo:** Permite escalado horizontal elástico sin colisiones de socket.
* **P2: Config Server vs Hardcoded:** Separación de código y ambiente sin recompilar JARs.
* **P3: Desalojo no instantáneo:** Heartbeats cada 30s y margen de 90s evitan inestabilidad de red (*flapping*).
* **P4: Esquema `lb://`:** No es DNS; es un identificador lógico que resuelve Spring Cloud LoadBalancer contra Eureka.
* **P5: Round Robin en Stateless:** Es óptimo porque los microservicios no guardan sesión; todo el estado reside en PostgreSQL.

---

## 📑 Diapositiva 8: Punto 5 - Rúbrica de Evaluación y Conclusiones
* **Cumplimiento 100% (20/20 pts):**
  * CRUD persistente en PostgreSQL: **Nivel A**
  * Config Server DEV/PROD: **Nivel A**
  * Registro y latidos Eureka: **Nivel A**
  * Gateway no bloqueante con `lb://`: **Nivel A**
  * Balanceo concurrente y tolerancia a fallos: **Nivel A**
  * Dominio propio ChaskiPC: **Nivel A**
