# 🖥️ Guion Oficial de Sustentación a Dos Voces - Unidad I (Sesiones S01 a S05)
## Sistema Distribuido Base: ChaskiPC - Hardware & Gaming Store
**Equipo:** Equipo 01 - ChaskiByte Systems (5to Ciclo - Grupo Único)  
**Institución:** Universidad Andina del Néstor Cáceres Velásquez / DTI Juliaca  
**Docente Evaluador:** Ing. Abel Ángel Sullón Macalupu  
**Curso:** Desarrollo de Aplicaciones Distribuidas (semestre-2026-2)  
**Tiempo Total Asignado:** 18 Minutos (8 min Exposición + 5 min Demo en Vivo + 5 min Preguntas)  

---

### 👥 Integrantes del Equipo y Reparto de Responsabilidades

| Integrante | Rol Técnico | Microservicio Transaccional | Microservicio No Transaccional | Enfoque Evaluativo |
| :--- | :--- | :--- | :--- | :--- |
| **Eliceo Parillo Mostajo** | Arquitectura Backend & DevOps | `pc-orden-ms` (Cabecera-Detalle, IGV 18%) | `pc-catalogo-ms` (Hardware y Stock) | Infraestructura, Config Server, Eureka, Gateway, Balanceo y Tolerancia a Fallos |
| **Laura Vargas Cristhian Paul** | Pasarela de Pagos & Seguridad | `pc-pago-ms` (Mercado Pago Sandbox) | `pc-auth-ms` (JWT / BCrypt) | Contratos REST, Validaciones HTTP (201/400/404), Seguridad y Persistencia |

---

## 📑 Diapositiva 1: Portada Oficial y Proyecto Sello
* **Tiempo:** Minuto 0:00 a 1:00
* **Voz de Apertura:** Eliceo Parillo Mostajo y Cristhian Paul Laura Vargas
* **Puntos Clave:**
  * Bienvenida al jurado evaluador y presentación del equipo *ChaskiByte Systems*.
  * Presentación del proyecto sello **ChaskiPC**: Plataforma de e-commerce distribuida para hardware gamer y componentes de alta gama.
  * Declaración de arquitectura orientada a microservicios autónomos, siguiendo los principios de *The Twelve-Factor App*.

---

## 📑 Diapositiva 2: Dominio ChaskiPC y Asignación de Roles por Integrante
* **Tiempo:** Minuto 1:00 a 2:30 (Habla Eliceo Parillo)
* **Puntos Clave:**
  * Justificación del negocio: Catálogo especializado de CPUs, GPUs, placas madre y SSDs; compras con cálculo de impuestos peruanos (IGV 18%) y pasarela de pagos.
  * Segregación de microservicios:
    * **Eliceo:** `pc-orden-ms` (Gestión de órdenes de compra con cabecera y detalle) + `pc-catalogo-ms` (Catálogo de hardware y control de inventario).
    * **Cristhian Paul:** `pc-pago-ms` (Procesamiento de pagos con tarjeta y webhooks de Mercado Pago) + `pc-auth-ms` (Gestión de usuarios y tokens JWT).
  * Repositorio oficial con topics configurados: `https://github.com/jaisesasaki24-cloud/ChaskiByte-Systems`.

---

## 📑 Diapositiva 3: Arquitectura Base Distribuida (Cuatro Capas)
* **Tiempo:** Minuto 2:30 a 4:00 (Habla Eliceo Parillo)
* **Puntos Clave:**
  * **Capa 1 - Clientes:** SPA Frontend, Consolas PowerShell y Postman.
  * **Capa 2 - Enrutamiento Central:** Spring Cloud Gateway reactivo en puerto **18080** (DEV) / **28080** (PROD). Cero acceso directo a microservicios.
  * **Capa 3 - Núcleo de Infraestructura:**
    * *Service Registry:* Netflix Eureka Server (`pagatu-eureka`) en puerto **8761**.
    * *Config Server:* Spring Cloud Config (`pagatu-config`) en puerto **8888** con fallback local y Git.
  * **Capa 4 - Microservicios & Persistencia:**
    * `pc-catalogo-ms` (puerto **8081**).
    * `pc-orden-ms` Instancia 1 (puerto **8082**) e Instancia 2 (puerto **8083**) en balanceo dinámico Round-Robin.
    * Base de datos PostgreSQL en contenedor Docker (`chaskipc-db-orden`) en puerto **5433**.
  * **Observabilidad:** Prometheus (**19090**) scraping métricas vía Eureka + Grafana (**13000**).

---

## 📑 Diapositiva 4: Fichas Técnicas y Contratos REST Segregados
* **Tiempo:** Minuto 4:00 a 6:00 (Habla Cristhian Paul Laura)
* **Puntos Clave:**
  * **Microservicios de Eliceo:**
    * `pc-catalogo-ms`: Endpoints `GET /api/v1/productos`, `GET /api/v1/categorias`, `POST /api/v1/productos`.
    * `pc-orden-ms`: Modelo Cabecera-Detalle (`Orden` -> `DetalleOrden`). Endpoints `GET /api/v1/ordenes`, `GET /api/v1/ordenes/{id}`, `POST /api/v1/ordenes`.
  * **Microservicios de Cristhian Paul:**
    * `pc-pago-ms`: Endpoint transaccional `POST /api/v1/pagos` con payload de tarjeta, monto y token de seguridad, integrado a sandbox.
    * `pc-auth-ms`: Endpoints `POST /api/v1/auth/login` y `POST /api/v1/auth/register` emitiendo JWT con expiración controlada.
  * Estandarización de códigos de respuesta HTTP: `200 OK`, `201 Created`, `400 Bad Request` con mensajes legibles, y `404 Not Found`.

---

## 📑 Diapositiva 5: Configuración Externalizada DEV vs PROD (Factor III)
* **Tiempo:** Minuto 6:00 a 7:00 (Habla Cristhian Paul Laura)
* **Puntos Clave:**
  * Cumplimiento estricto de la regla *Twelve-Factor App: Config*: El código es idéntico entre ambientes, los artefactos JAR no se modifican.
  * **Perfil DEV (`*-dev.yml`):**
    * Conexión a base de datos de desarrollo `localhost:5433/pagatu_orden_db`.
    * DDL Hibernate en `update` para iteración rápida.
    * Logging en nivel `DEBUG` y Actuator con endpoints abiertos (`health, info, metrics, prometheus`).
  * **Perfil PROD (`*-prod.yml`):**
    * Conexión aislada a red Docker interna `pagatu-prod-net`.
    * Credenciales administradas mediante variables de entorno del sistema (`POSTGRES_USER`, `POSTGRES_PASSWORD`).
    * DDL Hibernate en `validate` para evitar alteraciones accidentales del esquema en producción.

---

## 📑 Diapositiva 6: Evidencias Técnicas Reales del Sistema
* **Tiempo:** Minuto 7:00 a 8:00 (Alternado: Eliceo y Cristhian Paul)
* **Puntos Clave:**
  * **Evidencia Eureka:** Captura de pantalla real del dashboard Eureka en `:8761` con `PAGATU-GATEWAY`, `PAGATU-CONFIG`, `PC-CATALOGO-MS` y las 2 instancias de `PC-ORDEN-MS` en estado `UP`.
  * **Evidencia PostgreSQL y PowerShell:** Consulta SQL `SELECT id, cliente, total, igv FROM ordenes;` mostrando registros persistidos con cálculo del 18% de IGV e inserciones concurrentes.

---

## 📑 Diapositiva 7: Guion de Sustentación a Dos Voces (Tabla 5 Oficial)
* **Estructura Minuto a Minuto de los 18 Minutos:**
  * **Min 00 - 04 (Eliceo Parillo):** Apertura, planteamiento del problema, arquitectura base, Eureka, Config Server y enrutamiento Gateway.
  * **Min 04 - 08 (Cristhian Paul Laura):** Fichas técnicas, contratos REST, modelo transaccional cabecera-detalle, perfiles DEV/PROD y validaciones.
  * **Min 08 - 13 (Demo en Vivo Compartida):**
    * *Cristhian Paul (2.5 min):* Ejecución de pruebas funcionales (Caso 201 Created, Caso 400 Bad Request, Caso 404 Not Found) y verificación en PostgreSQL.
    * *Eliceo (2.5 min):* Demostración de balanceo de carga Round-Robin con 4 peticiones y prueba de tolerancia a fallos apagando una instancia en vivo.
  * **Min 13 - 18 (Ronda de Preguntas Individuales):** Respuesta a las preguntas del docente según el balotario asignado.

---

## 📑 Diapositiva 8: Centro de Mando en Vivo (Live Demo Cockpit)
* **Tiempo:** Minuto 8:00 a 13:00 (Demostración Práctica)

### 🚀 Accesos Directos de Supervisión:
* **Eureka Service Registry:** http://localhost:8761
* **Gateway - Órdenes ChaskiPC:** http://localhost:18080/api/v1/ordenes
* **Gateway - Catálogo de Hardware:** http://localhost:18080/api/v1/productos
* **Config Server (Dev Profile):** http://localhost:8888/pagatu-orden-ms/dev
* **Grafana Dashboards:** http://localhost:13000 (admin / admin)
* **Prometheus Targets:** http://localhost:19090/targets

### 💻 Scripts de Ejecución Asignados:

#### [Ejecuta Cristhian Paul] Paso 1: Caso Éxito (201 Created) - Orden con IGV 18%
```powershell
$orden = @{
    cliente = "Eliceo Parillo y Cristhian Paul"
    tipoComprobante = "FACTURA"
    metodoPago = "MERCADO_PAGO"
    detalles = @(
        @{ productoId = 1; nombreProducto = "AMD Ryzen 7 7800X3D"; precioUnitario = 1780.00; cantidad = 1 },
        @{ productoId = 4; nombreProducto = "Kingston Fury 1TB NVMe Gen4"; precioUnitario = 380.00; cantidad = 1 }
    )
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Post -Uri "http://localhost:18080/api/v1/ordenes" -Body $orden -ContentType "application/json"
```

#### [Ejecuta Cristhian Paul] Paso 2: Caso Validación (400 Bad Request)
```powershell
try {
    Invoke-RestMethod -Method Post -Uri "http://localhost:18080/api/v1/ordenes" -Body "{}" -ContentType "application/json"
} catch {
    Write-Host "Respuesta 400 capturada:" $_.Exception.Response.StatusCode.value__ -ForegroundColor Red
}
```

#### [Ejecuta Cristhian Paul] Paso 3: Caso Recurso No Encontrado (404 Not Found)
```powershell
try {
    Invoke-RestMethod -Uri "http://localhost:18080/api/v1/ordenes/99999"
} catch {
    Write-Host "Respuesta 404 capturada:" $_.Exception.Response.StatusCode.value__ -ForegroundColor Yellow
}
```

#### [Ejecuta Eliceo Parillo] Paso 4: Balanceo de Carga Round-Robin
```powershell
Write-Host "Enviando 4 solicitudes al Gateway para comprobar alternancia 8082 / 8083..." -ForegroundColor Cyan
1..4 | ForEach-Object {
    $r = Invoke-RestMethod -Uri "http://localhost:18080/api/v1/ordenes"
    Write-Host "Petición $_ respondida correctamente." -ForegroundColor Green
    Start-Sleep -Milliseconds 400
}
```

#### [Ejecuta Eliceo Parillo] Paso 5: Tolerancia a Fallos en Caliente
```powershell
# Detener manualmente la ventana de la instancia en puerto 8082 y ejecutar:
Invoke-RestMethod -Uri "http://localhost:18080/api/v1/ordenes"
# El Gateway redirige de forma transparente a la instancia 8083 sin corte de servicio.
```

---

## 📑 Diapositiva 9: Bitácora DevOps de Laboratorio DTI (7 Desafíos)
* **Tiempo:** Durante la ronda de preguntas o como soporte técnico.
* **Puntos Clave:**
  1. **Rutas Absolutas vs Relativas:** Automatización de `$PSScriptRoot` para que el proyecto corra en cualquier máquina de laboratorio sin tocar código.
  2. **Independencia de Entorno:** Creación de `iniciar_todo.ps1` en PowerShell puro sin exigir Python preinstalado.
  3. **Control de Versión JDK:** Verificación obligatoria de Java 21 para evitar fallos por versiones antiguas (Java 17/8).
  4. **Variables en PowerShell:** Corrección de inyección de `$env:SERVER_PORT` para levantar réplicas en paralelo.
  5. **Resiliencia de Config Server:** Implementación de `${CONFIG_REPO_PATH}` con fallback local a `file:./config-repo`.
  6. **Contenedores de Persistencia:** Script `iniciar_db.bat` con PostgreSQL en puerto 5433 sin entrar en conflicto con servicios locales en 5432.
  7. **Seguridad y Accesos:** Estandarización de credenciales por defecto seguras para evaluación en laboratorio (`admin` / `adminpassword`).

---

## 📑 Diapositiva 10: Balotario Teórico Asignado por Integrante (Tabla 4 Oficial)
* **Tiempo:** Minuto 13:00 a 18:00 (Ronda de Preguntas)

### 🎙️ Preguntas Asignadas a Eliceo Parillo Mostajo:
* **P1: ¿Por qué en un entorno distribuido el microservicio no debe fijar su puerto en código?**
  * *Respuesta:* Fijar el puerto acopla la aplicación a un socket físico impidiendo el escalado horizontal. Con puertos dinámicos (`${PORT:0}` o pasados por variable de entorno), múltiples instancias del mismo servicio pueden cohabitar en un mismo host sin colisión, registrándose autónomamente en Eureka.
* **P2: ¿Qué problema resuelve el servidor de configuración centralizado frente a `application.properties` en cada JAR?**
  * *Respuesta:* Resuelve la dispersión de configuración y el reprocesamiento de despliegues. Cambiar una URL o umbral no exige recompilar ni empaquetar los JARs; basta con actualizar el repositorio Git y ejecutar un `/actuator/refresh` sin tiempo de inactividad (*zero downtime*).

### 🎙️ Preguntas Asignadas a Laura Vargas Cristhian Paul:
* **P3: ¿Por qué el desalojo de una instancia en Eureka no es instantáneo al apagar el servicio?**
  * *Respuesta:* Eureka se rige por el Teorema CAP (prioriza Disponibilidad y Tolerancia a Particiones sobre Consistencia estricta). Maneja un ciclo de *heartbeats* (cada 30s) y una ventana de expiración de 90s para evitar desalojos prematuros provocados por micro-cortes temporales de red (*flapping*).
* **P4: ¿Por qué el Gateway usa `lb://NOMBRE-SERVICIO` en vez de `http://localhost:puerto`?**
  * *Respuesta:* Porque `lb://` no es un protocolo de transporte ni una resolución DNS; es un prefijo semántico que instruye al Spring Cloud LoadBalancer a consultar la lista de instancias activas en Eureka y aplicar balanceo de carga cliente (*client-side load balancing*).
* **P5: ¿Por qué Round Robin es adecuado para microservicios stateless pero insuficiente para stateful?**
  * *Respuesta:* En microservicios *stateless*, cualquier réplica puede atender cualquier solicitud porque el estado está en la base de datos PostgreSQL. En servicios *stateful* (que mantienen sesión local o memoria de usuario), un Round Robin simple enviaría la petición a una réplica sin contexto, rompiendo la transacción a menos que se use afinidad de sesión (*sticky sessions*).

---

## 📑 Diapositiva 11: Rúbrica de Evaluación y Conclusiones (20 / 20 pts)
* **Criterios de Evaluación Oficiales (Todos en Nivel A):**
  1. **CRUD Persistente y Modelo de Datos:** Cabecera-detalle en PostgreSQL con cálculo de IGV y manejo estricto de códigos HTTP (Nivel A: 4 pts).
  2. **Configuración Externalizada:** Separación nítida DEV vs PROD sin variables quemadas (Nivel A: 3 pts).
  3. **Registro y Descubrimiento Eureka:** Registro dinámico, metadata y visualización gráfica (Nivel A: 4 pts).
  4. **Enrutamiento y Balanceo Gateway:** Filtros reactivos y esquema `lb://` sin acoplamiento a IPs (Nivel A: 4 pts).
  5. **Tolerancia a Fallos y Alta Disponibilidad:** Continuidad de servicio ante caída forzada de una réplica (Nivel A: 3 pts).
  6. **Dominio Propio y Sustentación:** Presentación coordinada, roles definidos y dominio técnico del balotario (Nivel A: 2 pts).
  * **Puntaje Esperado del Equipo 01:** **20 / 20** 🏆
