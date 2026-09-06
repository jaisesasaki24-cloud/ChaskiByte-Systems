# 🅰️ Frontend Web ChaskiPC (Angular 18/19)
> Aplicación Single Page Application (SPA) para clientes finales de la plataforma e-commerce de hardware gamer ChaskiPC.

## 📅 Hoja de Ruta del Frontend (Desde Sesión S11)
Según el sílabo oficial de la asignatura **Desarrollo de Aplicaciones Distribuidas (2026-2)**:
* **Unidad 1 (S01 - S05):** Arquitectura de microservicios backend distribuida, Config Server, Eureka Service Discovery y API Gateway.
* **Unidad 2 (S06 - S10):** Resiliencia (Circuit Breaker Resilience4j), Seguridad perimetral JWT, Mensajería asíncrona (RabbitMQ/Kafka) y Observabilidad distribuida.
* **Unidad 3 (S11 - S16):** Integración Frontend SPA con Angular, pasarela de pago, carrito de compras reactivo y despliegue final en producción.

---

## 🏛️ Arquitectura de Módulos Planificada

```text
clients/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── catalogo/           # Grilla de componentes de PC, tarjetas de hardware y filtros por categoría
│   │   │   ├── orden-checkout/     # Resumen de orden, desglose de 18% IGV y facturación
│   │   │   ├── cliente-consulta/   # Formulario con autocompletado en tiempo real con RENIEC (DNI) y SUNAT (RUC)
│   │   │   └── pago-gateway/       # Modal de confirmación de pago
│   │   ├── models/
│   │   │   ├── producto.model.ts
│   │   │   ├── orden.model.ts
│   │   │   └── cliente.model.ts
│   │   └── services/
│   │       ├── catalogo.service.ts # Consumo: http://localhost:18080/api/v1/productos
│   │       ├── orden.service.ts    # Consumo: http://localhost:18080/api/v1/ordenes
│   │       └── cliente.service.ts  # Consumo: http://localhost:18080/api/v1/clientes
│   ├── index.html
│   └── main.ts
├── angular.json
├── package.json
└── tsconfig.json
```

---

## ⚡ Conexión al Backend
El cliente web se conecta de forma exclusiva a través del **API Gateway** (`http://localhost:18080`), abstrayendo las IPs y puertos individuales de los microservicios y aprovechando el balanceo de carga automático Round Robin.
