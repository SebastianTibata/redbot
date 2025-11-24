# RedBot

Sistema de gestión de redes sociales con arquitectura orientada a servicios (SOA).

## Características Principales

- 🤖 Gestión automatizada de cuentas de redes sociales
- 📊 **Dashboard de métricas** con estadísticas en tiempo real
- 🔐 **Sistema de seguridad avanzado** con autenticación JWT y llaves de acceso
- 📝 Gestión de tareas programadas
- 📜 Historial de ejecución
- 🎯 Arquitectura hexagonal y orientada a servicios

## Nuevas Funcionalidades

### 1. Dashboard de Métricas

Panel de control con estadísticas en tiempo real:
- Total de cuentas y tareas
- Distribución por estado (completadas, pendientes, en progreso, fallidas)
- Estadísticas por plataforma
- Tasa de éxito
- Visualización intuitiva con gráficos y métricas

**Acceso:** [http://localhost:3000/metrics.html](http://localhost:3000/metrics.html)

### 2. Sistema de Protección de Acceso

RedBot incluye un sistema de seguridad configurable con dos modalidades:

#### Autenticación Simétrica (Llave Compartida)
- Protección mediante llave maestra compartida
- Simple de configurar y usar
- Ideal para desarrollo o aplicaciones internas

#### Autenticación Asimétrica (RSA)
- Criptografía de clave pública/privada
- Mayor seguridad
- Prevención de replay attacks
- Ideal para producción

**Documentación completa:** Ver [SECURITY.md](SECURITY.md)

## Inicio Rápido

### 1. Configuración

Copie el archivo de configuración de ejemplo:

```bash
cp .env.example .env
```

### 2. Configurar Seguridad (Opcional)

Para habilitar la protección de acceso adicional:

```bash
python setup_security.py
```

Siga las instrucciones del asistente de configuración.

### 3. Iniciar los servicios

```bash
docker-compose up -d
```

### 4. Acceder a la aplicación

- **Frontend:** http://localhost:3000
- **Dashboard de Métricas:** http://localhost:3000/metrics.html
- **Documentación API:** http://localhost:8001/docs (ajustar puerto según servicio)

## Arquitectura

El sistema está compuesto por los siguientes servicios:

- **auth_service** (Puerto 8003): Autenticación y gestión de usuarios
- **account_service** (Puerto 8002): Gestión de cuentas de redes sociales
- **task_service** (Puerto 8004): Gestión de tareas
- **user_service** (Puerto 8001): Gestión de usuarios
- **executor_service** (Puerto 8005): Ejecución de tareas
- **frontend** (Puerto 3000): Interfaz de usuario
- **db**: Base de datos PostgreSQL

## Seguridad

RedBot implementa múltiples capas de seguridad:

1. **Autenticación JWT:** Tokens de sesión seguros
2. **Protección de acceso:** Sistema configurable de llaves (simétrica/asimétrica)
3. **Validación de datos:** Esquemas Pydantic
4. **Arquitectura hexagonal:** Separación de capas

Ver [SECURITY.md](SECURITY.md) para más detalles.

## Desarrollo

Para más información sobre la arquitectura y desarrollo, consulte [RedBot.md](RedBot.md).
