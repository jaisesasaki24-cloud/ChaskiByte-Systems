# Overrides de Configuración Local

Esta carpeta permite sobrescribir variables de entorno, puertos y credenciales para pruebas en laboratorios o máquinas locales sin modificar el repositorio versionado.

## Archivos Disponibles
- `dev-overrides.env.sample`: Plantilla de variables para Docker Compose y perfiles de Spring Boot.

## Uso
Copiar `dev-overrides.env.sample` a `dev-overrides.env` y definir los valores requeridos antes de ejecutar `iniciar_todo.bat`.
