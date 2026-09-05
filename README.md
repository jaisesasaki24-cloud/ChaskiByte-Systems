# 💻 ChaskiPC Hardware E-Commerce - Ecosistema Distribuido
> Plataforma de comercio electrónico distribuido para la cotización y venta de computadoras ensambladas, periféricos y piezas de hardware con verificación de stock en tiempo real y pasarela de pagos.
> **Sistema Distribuido Base Orientado a Producción (Unidad 1 Completa - Sesiones S01 a S05)**

[![Spring Boot 3.4.3](https://img.shields.io/badge/Spring%20Boot-3.4.3-brightgreen.svg)](https://spring.io/projects/spring-boot)
[![Spring Cloud 2024.0.0](https://img.shields.io/badge/Spring%20Cloud-2024.0.0-blue.svg)](https://spring.io/projects/spring-cloud)
[![Java 21](https://img.shields.io/badge/Java-21-orange.svg)](https://openjdk.org/projects/jdk/21/)
[![PostgreSQL 15](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)

---

## 👥 1. Datos del Equipo e Integrantes
* **Nombre del equipo:** Equipo 01 - ChaskiByte Systems
* **Sección:** 5to Ciclo - Grupo Único
* **Curso:** Desarrollo de Aplicaciones Distribuidas (2026-2)
* **Docente:** Ing. Abel Ángel Sullón Macalupu
* **Repositorio Oficial:** [https://github.com/jaisesasaki24-cloud/ChaskiByte-Systems](https://github.com/jaisesasaki24-cloud/ChaskiByte-Systems)

### 🏷️ Topics del Repositorio
`campus-juliaca` · `semestre-2026-2` · `linea-software` · `tipo-ps` · `dist` · `seccion-g1` · `grupo-01-chaskipc`

### 📋 Asignación de Roles y Microservicios
| Integrante | Rol en el Proyecto | Microservicio Transaccional | Microservicio No Transaccional |
| :--- | :--- | :--- | :--- |
| **Eliceo Parillo Mostajo** | Arquitectura backend, órdenes de compra y catálogo de hardware | `pc-orden-ms` (`pagatu-orden-ms`) | `pc-catalogo-ms` (`pagatu-catalogo-ms`) |
| **Laura Vargas Cristhian Paul** | Pasarela de pagos externa (Mercado Pago), seguridad y autenticación (Keycloak/JWT) | `pc-pago-ms` | `pc-auth-ms` |

---

## 🏛️ 2. Arquitectura del Sistema Distribuido Base (Unidad 1)

```mermaid
flowchart TB
    Client["Cliente Externo / Frontend / Swagger / PowerShell"]
    Gateway["API Gateway: pagatu-gateway<br/>Puerto 18080 (DEV) / 28080 (PROD)"]
    Eureka[("Eureka Server: pagatu-eureka<br/>Puerto 8761 (DEV) / 28761 (PROD)")]
    Config["Config Server: pagatu-config<br/>Puerto 8888 (DEV) / 28888 (PROD)")]
    Repo[("config-repo")]

    subgraph Microservicios["Microservicios de Negocio ChaskiPC"]
        Cat["pc-catalogo-ms (:8081)<br/>Categorías & Productos de Hardware"]
        O1["pc-orden-ms (Instancia 1 :8082)<br/>Cabecera-Detalle & IGV"]
        O2["pc-orden-ms (Instancia 2 :8083)<br/>Persistencia PostgreSQL"]
    end

    subgraph Database["Persistencia Relacional (Docker)"]
        PG1[("PostgreSQL db-orden :5433")]
    end

    subgraph Observabilidad["Stack de Observabilidad (Docker obs/)"]
        Prometheus["Prometheus (:19090)<br/>Eureka Service Discovery"]
        Grafana["Grafana (:13000)<br/>Dashboard JVM y Métricas"]
        Loki["Loki (:13100) & Promtail"]
    end

    Client -->|"Único punto de acceso HTTP"| Gateway
    Gateway -. "Descubre instancias vivas" .-> Eureka
    Gateway -->|"lb://pagatu-catalogo-ms"| Cat
    Gateway -->|"lb://pagatu-orden-ms (Round Robin)"| O1
    Gateway -->|"lb://pagatu-orden-ms (Round Robin)"| O2

    Cat -. "Auto-registro" .-> Eureka
    O1 -. "Auto-registro" .-> Eureka
    O2 -. "Auto-registro" .-> Eureka
    Gateway -. "Auto-registro" .-> Eureka

    O1 --> PG1
    O2 --> PG1

    Gateway -. "Carga rutas" .-> Config
    O1 -. "Carga config" .-> Config
    Cat -. "Carga config" .-> Config
    Config --> Repo

    Prometheus -. "eureka_sd_configs" .-> Eureka
    Grafana --> Prometheus
    Grafana --> Loki
```

---

## 📂 3. Estructura del Repositorio

```text
ChaskiByte-Systems/
├── config-repo/                     # Repositorio centralizado de configuraciones (DEV y PROD)
│   ├── application.yml
│   ├── pagatu-gateway-dev.yml       # Rutas lb:// y reglas de Gateway
│   ├── pagatu-orden-ms-dev.yml      # DB PostgreSQL y Eureka Client
│   ├── pagatu-catalogo-ms-dev.yml   # Catálogo JPA y Eureka Client
│   └── ...
├── pagatu-config/                   # Spring Cloud Config Server (Puerto 8888)
├── pagatu-eureka/                   # Netflix Eureka Service Discovery (Puerto 8761)
├── pagatu-gateway/                  # Spring Cloud Gateway no bloqueante (Puerto 18080)
├── pagatu-catalogo-ms/              # Catálogo ChaskiPC: Categorías y Productos (Puerto 8081)
├── pagatu-orden-ms/                 # Órdenes ChaskiPC: Cabecera-Detalle e IGV (Puertos 8082, 8083)
├── obs/                             # Docker Compose de Observabilidad (Prometheus, Grafana, Loki)
│   ├── compose-dev.yml
│   ├── prometheus/
│   └── grafana/
├── infra/                           # Docker Compose de Producción Local (Red pagatu-prod-net)
│   └── compose.yml
├── BRIEF_TECNICO.md                 # Documento técnico oficial del proyecto sello ChaskiPC
├── S03_Equipo01_ParilloEliceo.pdf   # Informe de Sesión 03 (Eureka & Múltiples Instancias)
├── S04_Equipo01_ParilloEliceo.pdf   # Informe de Sesión 04 (API Gateway & Balanceo de Carga)
├── S05_Equipo01_ParilloEliceo.pdf   # Informe Oficial de Evaluación y Cierre de la Unidad I
├── iniciar_todo.bat                 # Lanzador automático de todas las consolas en Windows
└── README.md
```

---

## 🚀 4. Guía de Ejecución en Entorno Local (DEV)

### Requisitos Previos:
* **Java Development Kit (JDK 21)**
* **Docker Desktop** (para PostgreSQL y observabilidad)

### Paso 1: Levantar Bases de Datos y Observabilidad
```powershell
# Levantar PostgreSQL
cd "pagatu-orden-ms"
docker compose -f compose-dev.yml up -d

# Levantar Observabilidad (Prometheus + Grafana + Loki)
cd "../obs"
docker compose -f compose-dev.yml up -d
```

### Paso 2: Ejecutar los Servicios de Infraestructura y Negocio
Puedes hacer doble clic en `iniciar_todo.bat` o abrir terminales independientes en PowerShell:

```powershell
# 1. Config Server (Puerto 8888)
cd "pagatu-config"
.\mvnw.cmd spring-boot:run

# 2. Eureka Server (Puerto 8761)
cd "pagatu-eureka"
.\mvnw.cmd spring-boot:run

# 3. API Gateway - Punto Único de Acceso (Puerto 18080)
cd "pagatu-gateway"
.\mvnw.cmd spring-boot:run

# 4. Catálogo de Hardware (Puerto 8081)
cd "pagatu-catalogo-ms"
.\mvnw.cmd spring-boot:run

# 5. Órdenes ChaskiPC - Instancia 1 (Puerto 8082)
cd "pagatu-orden-ms"
.\mvnw.cmd spring-boot:run

# 6. Órdenes ChaskiPC - Instancia 2 (Puerto 8083)
cd "pagatu-orden-ms"
.\mvnw.cmd spring-boot:run -Dspring-boot.run.arguments="--server.port=8083"
```

---

## 🧪 5. Catálogo de Endpoints y Pruebas a través del Gateway (Puerto 18080)

### 🛒 Microservicio de Catálogo de Hardware (`pc-catalogo-ms`)
| Método | Endpoint vía Gateway | Descripción |
| :--- | :--- | :--- |
| `GET` | `http://localhost:18080/api/v1/categorias` | Lista categorías (Procesadores, GPUs, RAM, etc.) |
| `GET` | `http://localhost:18080/api/v1/productos` | Catálogo completo con stock y precios |
| `GET` | `http://localhost:18080/api/v1/productos?categoriaId=1` | Filtro de componentes por categoría |
| `GET` | `http://localhost:18080/api/v1/productos/sku/CPU-AMD-001` | Ficha técnica por SKU de hardware |
| `POST` | `http://localhost:18080/api/v1/productos` | Registra un nuevo componente de hardware |

### 📦 Microservicio de Órdenes (`pc-orden-ms`)
| Método | Endpoint vía Gateway | Descripción |
| :--- | :--- | :--- |
| `GET` | `http://localhost:18080/api/v1/ordenes` | Listar todas las órdenes (balanceado Round Robin) |
| `GET` | `http://localhost:18080/api/v1/ordenes/{id}` | Consultar orden por ID con detalle e IGV |
| `POST` | `http://localhost:18080/api/v1/ordenes` | Registrar orden con ítems, comprobante y pago |
| `PUT` | `http://localhost:18080/api/v1/ordenes/{id}/estado` | Actualizar estado (`PAGADO`, `CANCELADO`, etc.) |
| `DELETE` | `http://localhost:18080/api/v1/ordenes/{id}` | Eliminar orden |

```powershell
# Ejemplo: Crear orden estructurada con ítems por el Gateway
$orden = @{
    cliente = "Eliceo Parillo Mostajo"
    tipoComprobante = "FACTURA"
    metodoPago = "TARJETA"
    detalles = @(
        @{ productoId = 1; nombreProducto = "AMD Ryzen 7 7800X3D"; precioUnitario = 1780.00; cantidad = 1 },
        @{ productoId = 3; nombreProducto = "Corsair DDR5 32GB"; precioUnitario = 520.00; cantidad = 2 }
    )
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Post -Uri "http://localhost:18080/api/v1/ordenes" -Body $orden -ContentType "application/json"
```

---

## 📑 6. Entregables Académicos Oficiales
* 📄 [**`BRIEF_TECNICO.md`**](BRIEF_TECNICO.md): Ficha técnica oficial del proyecto sello ChaskiPC.
* 📄 [**`S03_Equipo01_ParilloEliceo.pdf`**](S03_Equipo01_ParilloEliceo.pdf): Informe de la Sesión 03 (Eureka Server, Múltiples Instancias, Observabilidad).
* 📄 [**`S04_Equipo01_ParilloEliceo.pdf`**](S04_Equipo01_ParilloEliceo.pdf): Informe de la Sesión 04 (API Gateway, Rutas `lb://` y Balanceo de Carga).
* 📄 [**`S05_Equipo01_ParilloEliceo.pdf`**](S05_Equipo01_ParilloEliceo.pdf): **Informe Oficial de Evaluación y Sustentación de la Unidad I** (Balotario de defensa teórico-práctica resuelto y rúbrica de 20 pts).
