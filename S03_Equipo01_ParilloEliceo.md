# INFORME DE ACTIVIDAD AUTÓNOMA: SESIÓN 03
## Registro, Descubrimiento y Ejecución Concurrente de Servicios
### Proyecto Sello: ChaskiPC Hardware E-Commerce

**Datos del estudiante y del equipo:**
* **Nombre del estudiante:** Eliceo Parillo Mostajo
* **Equipo:** Equipo 01 - ChaskiByte Systems
* **Sección:** 5to Ciclo - Grupo Único
* **Proyecto Sello:** ChaskiPC Hardware E-Commerce (Sistema Distribuido para la Venta de Computadoras y Componentes)
* **Sesión:** S03 - Registro, Descubrimiento y Ejecución Concurrente de Servicios
* **Rol o aporte realizado:** Arquitectura backend, gestión de órdenes de compra (`pc-orden-ms` / `pagatu-orden-ms`) y catálogo de hardware (`pc-catalogo-ms`). Migración a Config Client y Eureka Client, configuración centralizada en `config-repo`, despliegue simultáneo de dos instancias en paralelo y verificación de descubrimiento dinámico y persistencia compartida.
* **Link de GitHub:** https://github.com/jaisesasaki24-cloud/pagatu-orden-ms
* **Topics del repositorio:** `campus-juliaca`, `semestre-2026-2`, `linea-software`, `tipo-ps`, `dist`, `seccion-g1`, `grupo-01-chaskipc`

---

## 1. Evidencia Técnica

### 1.1 Config Server Operativo (`pagatu-config`)
Verificación del servidor de configuración centralizado entregando los perfiles de `dev` y `prod` en el puerto 8888 para los microservicios de ChaskiPC.

![Config Server](evidencia_1_config_server.png)
*Figura 1: Servidor `pagatu-config` (puerto 8888) en perfil native aprovisionando configuraciones centralizadas desde config-repo.*

---

### 1.2 Eureka Server Operativo (`pagatu-eureka`)
Verificación del servidor de descubrimiento y registro Eureka activo en el puerto 8761 en modo standalone.

![Eureka Server](evidencia_2_eureka_server.png)
*Figura 2: Servidor `pagatu-eureka` (puerto 8761) recibiendo registros y heartbeats de los microservicios de ChaskiPC.*

---

### 1.3 `pagatu-catalogo-ms` (`pc-catalogo-ms`) Registrado en Eureka
Verificación del microservicio de catálogo de hardware (CPUs, GPUs, placas madre, laptops) ejecutándose en el puerto 8081 y registrado correctamente.

![Catalogo MS](evidencia_3_catalogo_ms.png)
*Figura 3: Microservicio `pagatu-catalogo-ms` activo en el puerto 8081 y anunciado en Eureka con estado 204 UP.*

---

### 1.4 `pagatu-orden-ms` (`pc-orden-ms`) - Primera Instancia (Puerto 8082)
Arranque de la primera instancia del gestor de órdenes de compra de hardware, obteniendo puerto y base de datos PostgreSQL desde el Config Server.

![Orden MS Instancia 1](evidencia_4_orden_instancia1.png)
*Figura 4: Instancia 1 de `pagatu-orden-ms` iniciada en puerto 8082 y registrada como `pagatu-orden-ms:8082`.*

---

### 1.5 `pagatu-orden-ms` (`pc-orden-ms`) - Segunda Instancia (Puerto 8083)
Despliegue concurrente de la segunda réplica de órdenes de ChaskiPC mediante `$env:SERVER_PORT=8083` para atender alta demanda de compras.

![Orden MS Instancia 2](evidencia_5_orden_instancia2.png)
*Figura 5: Instancia 2 de `pagatu-orden-ms` iniciada en puerto 8083 y registrada como `pagatu-orden-ms:8083`.*

---

### 1.6 Dashboard Web de Eureka (`http://localhost:8761`)
Comprobación de catálogo unificado en la interfaz web de Eureka mostrando descubrimiento multi-instancia de los servicios de ChaskiPC.

![Eureka Web Dashboard](evidencia_6_eureka_web_dashboard.png)
*Figura 6: Dashboard web de Eureka evidenciando `PAGATU-CATALOGO-MS` (1 instancia) y `PAGATU-ORDEN-MS` (2 instancias de compra) en estado UP.*

---

### 1.7 Verificación Integral por PowerShell (Config + Eureka + CRUD)
Comprobación del flujo completo: entrega HTTP del Config Server, consulta a `/eureka/apps` y persistencia relacional cruzada de órdenes de compra (POST en 8082 registrando compra de PC y GET en 8083 consultando la orden creada).

![Pruebas CRUD PowerShell](evidencia_7_pruebas_crud_powershell.png)
*Figura 7: Salida de PowerShell con usuario, fecha/hora, verificación JSON de Config Server, catálogo Eureka y CRUD concurrente exitoso.*

---


---

### 1.8 Observabilidad Integral (Prometheus + Grafana - Bonificación Opcional)
Se integró el stack de observabilidad en Docker (`obs/compose-dev.yml`) con **Prometheus** (puerto `19090`) y **Grafana** (puerto `13000`), configurados con descubrimiento dinámico vía Eureka (`eureka_sd_configs`) y aprovisionamiento automático de métricas JVM y Spring Boot para ChaskiPC. Ambos microservicios (`pc-orden-ms` y `pc-catalogo-ms`) exponen sus métricas en `/actuator/prometheus` mediante `micrometer-registry-prometheus`.

* **Prometheus:** [http://localhost:19090](http://localhost:19090) (Targets automáticos en `/targets`).
* **Grafana Dashboard:** [http://localhost:13000](http://localhost:13000) (Dashboard ChaskiPC con Uptime, Memoria JVM Heap y Peticiones HTTP).

## 2. Comprensión del Patrón (Service Registry)

### ¿Por qué un componente que consulta el registro ya no necesita una lista de direcciones escrita a mano para encontrar ninguna de las dos instancias de pagatu-orden-ms, aunque ambos puertos sean fijos y elegidos a mano?

El patrón **Service Registry (Eureka)** introduce una capa de abstracción basada en identificadores lógicos (`spring.application.name`):

1. **Abstracción por Nombre Lógico:** En la arquitectura de ChaskiPC, los componentes clientes (como el API Gateway, o `pc-pago-ms` consultando detalles de orden) no se comunican directamente con `localhost:8082` ni `localhost:8083`. En su lugar, solicitan a Eureka: *"Dame las instancias disponibles de `PAGATU-ORDEN-MS`"*.
2. **Autorregistro Dinámico:** Cada instancia al iniciar publica automáticamente sus metadatos (IP, puerto y estado de salud). Eureka mantiene actualizado el catálogo mediante *heartbeats* periódicos cada 30 segundos.
3. **Descubrimiento y Balanceo en Memoria:** El componente que consulta el registro descarga la lista de nodos y aplica un balanceador de carga del lado del cliente (Spring Cloud LoadBalancer con Round Robin) para distribuir el tráfico de órdenes de compra entre el puerto 8082 y 8083.
4. **Desacoplamiento Total:** Aunque los puertos sean fijos y elegidos a mano en DEV, el cliente nunca los tiene codificados (*hardcoded*). Si se agregan réplicas adicionales para soportar eventos de alta demanda (como promociones de ensamblaje de PCs) o si los servicios se mueven a contenedores Docker, el sistema continúa funcionando sin necesidad de modificar ni una sola línea de código o configuración en los servicios consumidores.

---

## 3. Error o Hallazgo Diagnosticado

* **Descripción del Problema:** Al compilar y arrancar `pagatu-orden-ms`, se presentó el error `Failed to configure a DataSource: 'url' attribute is not specified` y la aplicación fallaba al iniciar. Adicionalmente, en los archivos fuente Java figuraba el error de compilación `illegal character: '﻿'`.
* **Causa Raíz:** 
  1. Los archivos fuente tenían caracteres de marca de orden de bytes (*UTF-8 with BOM*) agregados por el editor de texto.
  2. En el archivo `pom.xml` faltaban las dependencias de `spring-cloud-starter-config` y `spring-cloud-starter-netflix-eureka-client`, lo que impedía que Spring Boot procesara la directiva `spring.config.import` para descargar la configuración de PostgreSQL (`orden_db`) desde `pagatu-config`.
* **Solución Implementada:** 
  Se ejecutó un script en PowerShell para limpiar el carácter BOM (`﻿`) de los archivos `.java`. Luego, se actualizaron las dependencias en `pom.xml` integrando el BOM `spring-cloud-dependencies` (versión `2024.0.0`) y las librerías de Config y Eureka Client, permitiendo que `pagatu-orden-ms` inicie correctamente conectado a su configuración remota en `config-repo`.

---

## 4. Reflexión Técnica Breve

**¿Por qué el registro y descubrimiento de servicios es un prerrequisito para el Gateway y el balanceo de carga que se construyen en S4?**

> El registro y descubrimiento de servicios es un prerrequisito indispensable porque el API Gateway de ChaskiPC no debe estar acoplado a direcciones IP ni a puertos estáticos de la infraestructura. En nuestra plataforma de e-commerce de hardware, las órdenes y pagos escalan horizontalmente según la demanda de compras. Eureka provee la tabla de enrutamiento viva y centralizada que el Gateway consulta en tiempo real para resolver rutas dinámicas. Sin el Service Registry, sería imposible balancear la carga automáticamente (Round Robin) entre las réplicas de `pc-orden-ms` y `pc-catalogo-ms`, o redirigir el tráfico ante la caída de un nodo sin tener que reescribir y reiniciar manualmente la configuración del Gateway.

---

## 5. Preguntas de Defensa

1. **¿Por qué `pagatu-eureka` no se registra a sí mismo (`register-with-eureka: false`)?**  
   Porque opera como un servidor de registro central *standalone*. Si intentara registrarse a sí mismo, emitiría peticiones fallidas continuas buscando réplicas de clúster inexistentes, generando sobrecarga innecesaria en los logs.
2. **¿Qué pasaría si intentaras levantar la segunda instancia de `pagatu-orden-ms` sin el override `--server.port=8083`?**  
   Se produciría una excepción `java.net.BindException: Address already in use` (`PortAlreadyInUseException`), dado que dos procesos no pueden escuchar en el mismo socket TCP (8082).
3. **¿Cómo verificaste que `pagatu-orden-ms` quedó correctamente registrado, y no solo que el proceso arrancó?**  
   Consultando la API REST de Eureka (`/eureka/apps`) y el Dashboard web, corroborando que ambas instancias aparecen con estado `UP` y con sus `instanceId` diferenciados (`pagatu-orden-ms:8082` y `pagatu-orden-ms:8083`).
4. **¿Qué le pasa a una instancia en el dashboard de Eureka si dejas de enviarle heartbeat (Ctrl+C)?**  
   Eureka deja de recibir los latidos de renovación (cada 30s). Al expirar el tiempo de arrendamiento (*lease expiration* de 90s), el servidor elimina la instancia de su catálogo para evitar redirigir tráfico a un servicio caído.
5. **¿Por qué el nombre lógico (`spring.application.name`) es el mismo dato que ya usa `pagatu-config` desde S2?**  
   Porque actúa como la clave primaria canónica en el ecosistema Spring Cloud: Config Server lo usa para asociar el archivo YAML en el repositorio (`pagatu-orden-ms-dev.yml`) y Eureka lo emplea como el Service ID (VIPAddress) para el descubrimiento.

---

## Anexo: Feedback de la Sesión

1. **¿Cuál es el aprendizaje más importante que te llevas de la clase de hoy?**  
   Comprender cómo el Service Registry (Eureka) permite que los microservicios de ChaskiPC se descubran dinámicamente usando únicamente su nombre lógico, abstrayendo por completo los puertos e IPs físicas.
2. **¿Qué punto de la clase te resultó más confuso o te dejó con dudas?**  
   El funcionamiento del *Self-Preservation Mode* de Eureka y cómo se configuran los umbrales de expiración del *heartbeat* en entornos distribuidos.
3. **¿Tienes alguna pregunta que te gustaría que sea respondida la siguiente clase?**  
   ¿Cómo gestiona Spring Cloud Gateway la distribución del tráfico cuando una instancia registrada en Eureka comienza a responder con errores HTTP 500 pero sigue enviando *heartbeats* como `UP`?
4. **Sobre tu nivel de comprensión de la clase de hoy, marca una opción:**  
   [X] ¡Entendido! - Lo domino y podría explicarlo.  
   [ ] Más o menos. - Entendí la idea general, pero tengo dudas.  
   [ ] Necesito ayuda. - Me siento perdido/a con este tema.
5. **¿Cómo puedo ayudarte a comprender mejor el tema?**  
   Incluyendo diagramas de secuencia visuales sobre el ciclo de vida del *heartbeat* y la resolución de rutas en el Gateway.
6. **Pensando en tu participación y esfuerzo en la clase de hoy, ¿cómo te autoevaluarías?**  
   [X] Muy Comprometido/a: Me esforcé al máximo.  
   [ ] Comprometido/a: Sé que podría haberme esforzado un poco más.  
   [ ] Poco Comprometido/a: Hoy no di mi mejor esfuerzo.
7. **Mi satisfacción con la clase fue:**  
   10 / 10
