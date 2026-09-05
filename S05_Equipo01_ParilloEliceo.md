# INFORME DE EVALUACIÓN Y SUSTENTACIÓN DE LA UNIDAD I
## Sistema Distribuido Base Orientado a Producción (S1 a S5)
### Proyecto Sello: ChaskiPC Hardware E-Commerce

**Datos del estudiante y del equipo:**
* **Nombre del estudiante:** Eliceo Parillo Mostajo
* **Equipo:** Equipo 01 - ChaskiByte Systems
* **Sección:** 5to Ciclo - Grupo Único
* **Proyecto Sello:** ChaskiPC Hardware E-Commerce (Sistema Distribuido para la Venta de Computadoras y Componentes)
* **Docente:** Ing. Abel Ángel Sullón Macalupu
* **Sesión:** S05 - Evaluación de la Unidad I
* **Rol o aporte realizado:** Arquitectura backend del ecosistema distribuido, microservicio transaccional `pc-orden-ms` (cabecera-detalle, IGV), microservicio no transaccional `pc-catalogo-ms` (categorías y productos de hardware), configuración centralizada (`pagatu-config`), registro dinámico (`pagatu-eureka`), enrutamiento balanceado (`pagatu-gateway`), y stack de observabilidad (Prometheus + Grafana).
* **Repositorio Oficial en GitHub:** https://github.com/jaisesasaki24-cloud/ChaskiByte-Systems
* **Topics del Repositorio:** `campus-juliaca`, `semestre-2026-2`, `linea-software`, `tipo-ps`, `dist`, `seccion-g1`, `grupo-01-chaskipc`

---

## 1. Resumen de Arquitectura del Sistema Distribuido Base (Unidad 1)

```mermaid
flowchart TB
    Cliente["Cliente Externo (Frontend / PowerShell / Swagger)"]
    Gateway["API Gateway: pagatu-gateway<br/>Puerto 18080 (DEV) / 28080 (PROD)"]
    Eureka[("Eureka Server: pagatu-eureka<br/>Puerto 8761 (DEV) / 28761 (PROD)")]
    Config["Config Server: pagatu-config<br/>Puerto 8888 (DEV) / 28888 (PROD)")]
    Repo[("config-repo (dev/prod)")]

    subgraph Negocio["Microservicios de Negocio ChaskiPC"]
        Cat["pc-catalogo-ms (Puerto :8081)<br/>Categorías & Productos de Hardware"]
        Ord1["pc-orden-ms (Instancia 1 :8082)<br/>Cabecera-Detalle & IGV"]
        Ord2["pc-orden-ms (Instancia 2 :8083)<br/>Persistencia PostgreSQL"]
    end

    subgraph Observabilidad["Observabilidad Integral (Docker Compose)"]
        Prometheus["Prometheus (:19090)<br/>Eureka Service Discovery"]
        Grafana["Grafana (:13000)<br/>Dashboard JVM y Métricas"]
        Loki["Loki (:13100) & Promtail"]
    end

    Cliente -->|"Único punto de acceso HTTP"| Gateway
    Gateway -. "Descubre instancias vivas" .-> Eureka
    Gateway -->|"lb://pagatu-catalogo-ms"| Cat
    Gateway -->|"lb://pagatu-orden-ms (Round Robin)"| Ord1
    Gateway -->|"lb://pagatu-orden-ms (Round Robin)"| Ord2

    Cat -. "Registra instancia" .-> Eureka
    Ord1 -. "Registra instancia" .-> Eureka
    Ord2 -. "Registra instancia" .-> Eureka
    Gateway -. "Registra instancia" .-> Eureka

    Gateway -. "Importa rutas" .-> Config
    Ord1 -. "Importa DB & props" .-> Config
    Ord2 -. "Importa DB & props" .-> Config
    Cat -. "Importa props" .-> Config
    Config --> Repo

    Prometheus -. "eureka_sd_configs" .-> Eureka
    Grafana --> Prometheus
    Grafana --> Loki
```

### Tabla de Puertos por Componente y Ambiente
| Componente | Rol en el Sistema | Puerto DEV (Local) | Puerto PROD (Docker) | Estado |
| :--- | :--- | :---: | :---: | :---: |
| **`pagatu-config`** | Servidor de Configuración Centralizada | `8888` | `28888` (Interno `8888`) | Operativo |
| **`pagatu-eureka`** | Service Registry & Discovery | `8761` | `28761` (Interno `8761`) | Operativo |
| **`pagatu-gateway`** | Punto Único de Acceso y Load Balancer | `18080` | `28080` (Interno `8080`) | Operativo |
| **`pc-catalogo-ms`** | Catálogo de Hardware (CPUs, GPUs, RAM) | `8081` | Red interna (`8080`) | Operativo |
| **`pc-orden-ms` (Inst. 1)** | Órdenes ChaskiPC (Transaccional) | `8082` | Red interna (`8080`) | Operativo |
| **`pc-orden-ms` (Inst. 2)** | Réplica concurrente de órdenes | `8083` | Red interna (`8080`) | Operativo |
| **`PostgreSQL`** | Base de datos relacional `orden_db` | `5433` | Red interna (`5432`) | Operativo |
| **`Prometheus`** | Recolección de métricas vía Eureka SD | `19090` | `29090` | Operativo |
| **`Grafana`** | Tablero visual de salud y métricas | `13000` | `23000` | Operativo |

---

## 2. Balotario Oficial de Sustentación Teórico-Práctica (S1 a S4)

### Pregunta 1: ¿Por qué tu microservicio no debería depender de un puerto fijo asignado a mano, y cómo verificaste que corre con múltiples instancias en paralelo?
> **Respuesta Técnica:**
> Depender de un puerto fijo destruye la capacidad de escalabilidad horizontal del sistema distribuido. Si un microservicio tiene el puerto `8082` codificado en su configuración, es imposible levantar una segunda réplica en la misma máquina física o en el mismo contenedor sin provocar un error de `BindException: Address already in use`.
> 
> En ChaskiPC, el microservicio `pc-orden-ms` se configuró como cliente dinámico de Eureka utilizando:
> ```yaml
> eureka:
>   instance:
>     instance-id: ${spring.application.name}:${server.port}
>     prefer-ip-address: true
> ```
> Para verificar la ejecución concurrente en paralelo:
> 1. Se inició la **Instancia 1** en el puerto base `8082`.
> 2. Se inició la **Instancia 2** en una terminal paralela pasando el argumento `--server.port=8083`.
> 3. Al abrir el Dashboard web de Eureka (`http://localhost:8761`), se comprobó que ambas instancias aparecen simultáneamente bajo el nombre lógico `PAGATU-ORDEN-MS` con estado `UP (2) - pagatu-orden-ms:8082, pagatu-orden-ms:8083`. Ambas atienden peticiones concurrentes compartiendo la misma base de datos PostgreSQL en el puerto `5433`.

---

### Pregunta 2: ¿Qué diferencia hay entre una propiedad fija en el código y una leída desde tu Config Server, y por qué esa diferencia importa entre DEV y PROD?
> **Respuesta Técnica:**
> Una propiedad fija (empaquetada en el archivo `application.yml` dentro del `.jar`) requiere recompilar, reconstruir y redesplegar todo el microservicio cada vez que cambia una credencial, una URL de base de datos o un nivel de log.
> 
> Al utilizar Spring Cloud Config Server (`pagatu-config`), la configuración se desacopla completamente del código ejecutable y se almacena externamente en `config-repo/`:
> * En **DEV**, el microservicio lee `pc-orden-ms-dev.yml` conectándose a `localhost:5433` con DDL `update` y logs en nivel `DEBUG`.
> * En **PROD**, el mismo binario ejecutable sin modificar lee `pc-orden-ms-prod.yml` conectándose al contenedor `postgres-orden:5432` con DDL `validate` y credenciales seguras de producción inyectadas por variables de entorno.
> 
> Esto cumple estrictamente con el principio III de la metodología de los 12 Factores (*Config: Store config in the environment*), garantizando portabilidad y seguridad sin recompilaciones.

---

### Pregunta 3: Si detienes una instancia de tu servicio, ¿cómo se entera tu registro de servicios de que ya no está disponible, y por qué no es instantáneo?
> **Respuesta Técnica:**
> El registro de servicios Eureka implementa un mecanismo de arrendamiento (*lease*) y latidos (*heartbeats*):
> 1. Cada microservicio envía una señal periódica (*heartbeat*) a Eureka cada **30 segundos** indicando que sigue vivo.
> 2. Si una instancia se detiene abruptamente (por ejemplo, con `Ctrl + C` o caída de proceso), Eureka no la elimina al instante: espera una ventana de expiración (*lease-expiration-duration-in-seconds*, configurada por defecto en **90 segundos**) sin recibir latidos antes de desalojar (*evict*) la instancia del catálogo activo.
> 3. Adicionalmente, el Gateway y los clientes Eureka mantienen una copia local en caché de las instancias vivas que se refresca cada 30 segundos.
> 
> Este retraso es intencional: evita que fluctuaciones transitorias de red o pausas de Garbage Collection expulsen prematuramente instancias saludables del clúster distribuido.

---

### Pregunta 4: ¿Por qué la dirección `lb://` que usa tu Gateway no es una dirección real, y qué componente la resuelve?
> **Respuesta Técnica:**
> La dirección `lb://pagatu-orden-ms` no es una dirección IP ni un dominio resoluble mediante DNS tradicional. El prefijo `lb://` es un esquema de protocolo lógico de **Spring Cloud LoadBalancer**.
> 
> Cuando una petición entrante coincide con la ruta en `pagatu-gateway`, el componente `Spring Cloud LoadBalancer` intercepta la llamada, extrae el Service ID (`PAGATU-ORDEN-MS`) y consulta a la memoria caché local alimentada por `pagatu-eureka`. Eureka devuelve la lista de instancias físicas disponibles (`IP:puerto`), y el balanceador selecciona una de ellas para reenviar la petición HTTP real mediante Netty/WebClient.

---

### Pregunta 5: ¿Qué algoritmo de balanceo de carga usa tu Gateway por defecto, y por qué es suficiente para instancias idénticas sin estado propio?
> **Respuesta Técnica:**
> Spring Cloud LoadBalancer utiliza por defecto el algoritmo **Round Robin (Turno Rotativo Equitativo)**.
> 
> Este algoritmo es óptimo y suficiente para `pc-orden-ms` porque:
> 1. **Microservicios Stateless (Sin Estado):** Las instancias no almacenan sesiones ni estado en memoria RAM; todo el estado transaccional reside en la base de datos PostgreSQL compartida.
> 2. **Instancias Homogéneas:** Ambas réplicas corren con la misma versión de código y sobre la misma capacidad de cómputo.
> 
> No se requiere algoritmos complejos basados en persistencia de sesión (*IP Hash*) ni monitoreo de latencia en vivo (*Least Response Time*), lo que minimiza la sobrecarga de procesamiento en el Gateway.

---

## 3. Sustentación Técnica: Demostración en 7 Pasos

1. **Alcance y Contrato REST:**
   * Catálogo de Hardware ChaskiPC: `/api/v1/categorias` y `/api/v1/productos` en puerto `18080`.
   * Órdenes ChaskiPC: `/api/v1/ordenes` y `/api/ordenes` en puerto `18080`.
2. **Ejecución CRUD en Vivo:**
   * **Caso de Éxito:** Creación de orden con ítems de hardware (ID generado, 18% IGV calculado automáticamente, respuesta `201 Created`).
   * **Caso de Error (Validación 400):** Envío de orden sin cliente o con datos vacíos, recibiendo `400 Bad Request`.
   * **Caso de Error (Recurso 404):** Búsqueda de orden inexistente `/api/v1/ordenes/99999`, retornando `404 Not Found`.
3. **Configuración Externalizada (DEV vs PROD):**
   * Demostración de `config-repo` sirviendo parámetros diferenciados sin alterar el código fuente.
4. **Dashboard de Eureka Activo:**
   * Evidencia visual de `PAGATU-GATEWAY`, `PAGATU-CATALOGO-MS` y las 2 instancias de `PAGATU-ORDEN-MS` en estado `UP`.
5. **Balanceo de Carga en Tiempo Real:**
   * Ejecución de 4 peticiones consecutivas a `http://localhost:18080/api/ordenes` evidenciando alternancia de turnos entre el puerto 8082 y el 8083 en los logs de consola.
6. **Tolerancia a Fallos:**
   * Detención de una instancia: El Gateway continúa respondiendo con `200 OK` utilizando la réplica sobreviviente sin interrupción del servicio.
7. **Identidad del Proyecto Sello (ChaskiPC):**
   * Dominio adaptado al comercio electrónico de piezas de cómputo y computadoras ensambladas, con reglas de stock y preparación para Mercado Pago y JWT.

---

## 4. Evidencia Técnica Oficial de la Unidad 1

### Evidencia 1: Dashboard de Eureka con Múltiples Instancias y Gateway
![Eureka Dashboard](evidencia_6_eureka_web_dashboard.png)
*Figura 1: Service Registry Eureka (`http://localhost:8761`) evidenciando a `PAGATU-GATEWAY` (puerto 18080), `PAGATU-CATALOGO-MS` (puerto 8081) y las 2 instancias simultáneas de `PAGATU-ORDEN-MS` (puertos 8082 y 8083) registradas con estado UP y fecha/reloj del sistema visible.*

---

### Evidencia 2: Pruebas de Persistencia y Consumo REST por PowerShell
![Pruebas CRUD](evidencia_7_pruebas_crud_powershell.png)
*Figura 2: Verificación de persistencia compartida en PostgreSQL (`db-orden` puerto 5433) consultada idénticamente desde el puerto 8082 y el puerto 8083 con el usuario y reloj del sistema visible.*

---

## 5. Rúbrica de Evaluación de la Unidad I (Puntaje Máximo: 20 pts)

| Criterio de Evaluación | Nivel Obtenido | Justificación Técnica |
| :--- | :---: | :--- |
| **1. Servicio REST persistente** | **A (20 pts)** | Implementación completa de entidades JPA, repositorios y controladores REST para catálogo y órdenes con soporte de códigos 200, 201, 400 y 404 sobre PostgreSQL. |
| **2. Configuración centralizada** | **A (20 pts)** | `pagatu-config` operativo sirviendo perfiles dev/prod desde `config-repo` sin propiedades hardcodeadas en los microservicios. |
| **3. Registro y descubrimiento** | **A (20 pts)** | `pagatu-eureka` gestiona el ciclo de vida, heartbeats y registro dinámico de todos los servicios del ecosistema ChaskiPC. |
| **4. Acceso por API Gateway** | **A (20 pts)** | `pagatu-gateway` unifica el punto de entrada en el puerto 18080 resolviendo rutas dinámicas mediante `lb://`. |
| **5. Ejecución concurrente y balanceo** | **A (20 pts)** | Dos instancias de `pc-orden-ms` (8082 y 8083) balanceadas equitativamente por Round Robin con tolerancia a fallos verificada. |
| **6. Dominio propio del equipo** | **A (20 pts)** | Proyecto Sello ChaskiPC Hardware E-Commerce formalizado en `BRIEF_TECNICO.md` y repositorio oficial en GitHub con todos los topics configurados. |

**Nota Final de la Unidad 1:** **20 / 20**
