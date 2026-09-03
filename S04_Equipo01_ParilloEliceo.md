# INFORME DE ACTIVIDAD AUTÓNOMA: SESIÓN 04
## Punto Único de Acceso y Distribución de Tráfico (API Gateway & Load Balancing)
### Proyecto Sello: ChaskiPC Hardware E-Commerce

**Datos del estudiante y del equipo:**
* **Nombre del estudiante:** Eliceo Parillo Mostajo
* **Equipo:** Equipo 01 - ChaskiByte Systems
* **Sección:** 5to Ciclo - Grupo Único
* **Proyecto Sello:** ChaskiPC Hardware E-Commerce (Sistema Distribuido para la Venta de Computadoras y Componentes)
* **Sesión:** S04 - Punto Único de Acceso y Distribución de Tráfico
* **Rol o aporte realizado:** Construcción de `pagatu-gateway` (Spring Cloud Gateway en puerto 18080), externalización de rutas dinámicas en `config-repo`, resolución mediante `lb://` sobre `pagatu-eureka` y balanceo de carga Round Robin entre réplicas de `pc-orden-ms` y `pc-catalogo-ms`.
* **Link de GitHub:** https://github.com/jaisesasaki24-cloud/pagatu-orden-ms
* **Topics del repositorio:** `campus-juliaca`, `semestre-2026-2`, `linea-software`, `tipo-ps`, `dist`, `seccion-g1`, `grupo-01-chaskipc`

---

## 1. Evidencia Técnica

### 1.1 `pagatu-gateway` Operativo y Registrado en Eureka
Verificación del API Gateway (Spring Cloud Gateway) iniciado en el puerto 18080 en DEV, anunciado ante el Service Registry `pagatu-eureka` (puerto 8761).

![Eureka Gateway](evidencia_6_eureka_web_dashboard.png)
*Figura 1: Servidor de descubrimiento Eureka registrando a `PAGATU-GATEWAY` (puerto 18080) junto a los microservicios de catálogo y órdenes.*

---

### 1.2 Rutas hacia `pagatu-catalogo-ms` Vía Gateway
Prueba de consulta de componentes de hardware (CPUs, GPUs, periféricos) a través del punto único de acceso (`http://localhost:18080/api/v1/productos`), sin que el cliente conozca los puertos 8080 ni 8081.

![Catalogo Gateway](evidencia_3_catalogo_ms.png)
*Figura 2: Peticiones HTTP resueltas por `pagatu-gateway` hacia el catálogo de hardware mediante `lb://pagatu-catalogo-ms`.*

---

### 1.3 Ruta Nueva hacia `pagatu-orden-ms` en `config-repo`
Definición de la ruta de compras en `pagatu-gateway-dev.yml` hacia `lb://pagatu-orden-ms` (`/api/ordenes/**`) y comprobación de consumo por HTTP sin invocar puertos directos.

![Config Gateway](evidencia_1_config_server.png)
*Figura 3: `pagatu-config` suministrando las rutas activas de ChaskiPC al Gateway desde `config-repo`.*

---

### 1.4 Distribución de Tráfico y Balanceo de Carga (Round Robin)
Verificación de múltiples peticiones consecutivas enviadas al Gateway (`18080`) que son repartidas equitativamente entre la Instancia 1 (puerto 8082) y la Instancia 2 (puerto 8083) de `pagatu-orden-ms`.

![Balanceo de Carga](evidencia_7_pruebas_crud_powershell.png)
*Figura 4: Salida de pruebas en PowerShell demostrando la alternancia de turnos y persistencia compartida en PostgreSQL.*

---

## 2. Comprensión del Patrón (API Gateway & Load Balancing)

### 2.1 ¿Por qué el cliente deja de conocer puertos individuales y cómo elige el balanceador la instancia?
1. **Punto Único de Contacto (*Single Point of Contact*):** El cliente externo (aplicación web, móvil o script de prueba) solo se comunica con `localhost:18080`. Se abstrae completamente la topología de la red interna.
2. **Resolución de Esquema `lb://`:** Cuando el Gateway recibe una petición en `/api/ordenes`, busca el predicado coincidente y lee el destino `lb://pagatu-orden-ms`. El prefijo `lb://` instruye a Spring Cloud LoadBalancer que consulte a Eureka para obtener la lista viva de instancias de ese servicio.
3. **Algoritmo Round Robin:** El balanceador distribuye las peticiones secuencialmente por turnos: la primera va a la instancia 1 (`8082`), la segunda a la instancia 2 (`8083`), y la tercera vuelve a la instancia 1.
4. **Tolerancia a Fallos Transparente:** Si una réplica se apaga, Eureka expira su *heartbeat* y el Gateway redirige el 100% del tráfico a las réplicas sanas restantes sin que el usuario reciba un error ni deba cambiar de URL.

---

## 3. Error o Hallazgo Diagnosticado

* **Descripción del Problema:** Al compilar `pagatu-gateway`, la aplicación arrojaba la excepción `AnnotationConfigReactiveWebServerApplicationContext cannot be cast to ServletWebServerApplicationContext` o entraba en conflicto con dependencias web tradicionales.
* **Causa Raíz:** Spring Cloud Gateway es un framework **no bloqueante y reactivo** construido sobre **Project Reactor y Netty**. Si el archivo `pom.xml` incluye `spring-boot-starter-web` (que incluye Apache Tomcat y Spring MVC sincrónico), se produce un choque de servidores embebidos.
* **Solución Implementada:** Se verificó que `pagatu-gateway/pom.xml` incluya exclusivamente `spring-cloud-starter-gateway` y `spring-cloud-starter-netflix-eureka-client`, permitiendo que Netty asuma el control del servidor HTTP en el puerto 18080 sin dependencias bloqueantes de Servlet.

---

## 4. Reflexión Técnica Breve

**¿Por qué agregar un microservicio nuevo al sistema no debería exigir que los clientes existentes cambien nada de su configuración?**

> El principio de desacoplamiento arquitectónico dicta que los consumidores de una API no deben estar acoplados a la infraestructura interna del proveedor. Gracias al API Gateway, los clientes externos únicamente conocen la URL base pública (`http://gateway:18080`). Cuando el equipo incorpora un nuevo microservicio (por ejemplo, `pc-pago-ms` para procesar cobros de hardware con Mercado Pago), únicamente se registra una nueva regla de enrutamiento en `config-repo/pagatu-gateway-dev.yml`. El Gateway actualiza dinámicamente sus rutas en caliente, permitiendo que las aplicaciones cliente comiencen a consumir el nuevo servicio inmediatamente sin reinstalar software, sin reconfigurar variables de entorno y sin desplegar actualizaciones en el cliente.

---

## 5. Preguntas de Defensa

1. **¿Por qué `lb://pagatu-catalogo-ms` no es una dirección real, y quién la resuelve?**  
   `lb://` es un identificador de protocolo lógico en Spring Cloud. No es una dirección IP resoluble por DNS. Lo resuelve `Spring Cloud LoadBalancer` consultando el catálogo de instancias registradas en `pagatu-eureka` bajo el nombre lógico `PAGATU-CATALOGO-MS`.
2. **¿Qué diferencia hay entre un `Path` que no coincide con ninguna ruta y un servicio de destino que está caído?**  
   Si el `Path` no coincide, el Gateway responde inmediatamente con `404 Not Found` porque ninguna ruta reclamó la URL. Si el servicio de destino está caído o no responde, el Gateway responde con `503 Service Unavailable` o `504 Gateway Timeout`.
3. **¿Por qué dos recursos del mismo microservicio (`/api/v1/categorias`, `/api/v1/productos`) necesitan dos rutas distintas?**  
   Porque el Gateway evalúa predicados basados en patrones de ruta (`Path`). Aunque ambos terminen en el mismo `uri: lb://pagatu-catalogo-ms`, cada patrón de endpoint puede requerir filtros específicos, políticas de caché o roles de seguridad diferenciados.
4. **Si detienes una instancia con Ctrl+C, ¿cuánto tiempo pasa hasta que el Gateway deja de enviarle tráfico?**  
   Pasan entre 30 y 90 segundos. Esto se debe a la ventana de expiración del *heartbeat* en Eureka (latido cada 30s y *lease expiration* de 90s) sumado al refresco de la caché local del LoadBalancer.
5. **¿Por qué agregar la ruta de `pagatu-orden-ms` no requirió tocar ninguna configuración de `pagatu-catalogo-ms`?**  
   Porque cada microservicio está completamente aislado y desacoplado. El Gateway centraliza el mapeo de rutas de forma modular en `config-repo`, permitiendo incorporar nuevos servicios sin afectar a los preexistentes.

---

## Anexo: Feedback de la Sesión

1. **¿Cuál es el aprendizaje más importante que te llevas de la clase de hoy?**  
   Comprender cómo el API Gateway unifica el acceso a todos los microservicios de ChaskiPC y aplica balanceo de carga automático sin exponer la topología interna.
2. **¿Qué punto de la clase te resultó más confuso o te dejó con dudas?**  
   La sincronización entre el refresco de rutas del Gateway y el tiempo de arrendamiento (*lease renewal*) de Eureka.
3. **¿Tienes alguna pregunta que te gustaría que sea respondida la siguiente clase?**  
   ¿Cómo se implementan filtros globales de autenticación JWT en Spring Cloud Gateway para validar tokens antes de reenviar la petición a los microservicios de negocio?
4. **Sobre tu nivel de comprensión de la clase de hoy, marca una opción:**  
   [X] ¡Entendido! - Lo domino y podría explicarlo.  
   [ ] Más o menos. - Entendí la idea general, pero tengo dudas.  
   [ ] Necesito ayuda. - Me siento perdido/a con este tema.
5. **¿Cómo puedo ayudarte a comprender mejor el tema?**  
   Incluyendo ejemplos prácticos de Rate Limiting y Circuit Breaker (Resilience4j) en el Gateway.
6. **Pensando en tu participación y esfuerzo en la clase de hoy, ¿cómo te autoevaluarías?**  
   [X] Muy Comprometido/a: Me esforcé al máximo.  
   [ ] Comprometido/a: Sé que podría haberme esforzado un poco más.  
   [ ] Poco Comprometido/a: Hoy no di mi mejor esfuerzo.
7. **Mi satisfacción con la clase fue:**  
   10 / 10
