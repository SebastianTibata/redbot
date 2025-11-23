# RedBot

Estoy creando un proyecto universitario que es una web para automatizar tareas para redes sociales( instagram, reddit, x) las funcionalidades serán las siguientes:

## Funcionalidades

1. Responder comentarios de forma automática
2. Publicaciones programadas
3. Moderar (Eliminar comentarios con insultos, filtrar spam, etc)

---

## Flujo de funcionamiento

### 1. Autenticación

a. El usuario accede a la web y se le presenta la página de login.  
b. El sistema valida el usuario y contraseña contra la base de datos.  
c. La contraseña está almacenada con hash **SHA-512**.  
d. Si es correcto, genera un **token de sesión (JWT o similar)**.  
e. El usuario es redirigido a la _Mainpage_.

### 2. Mainpage (Panel principal)

a. El usuario ve las cuentas ya vinculadas (Instagram, Reddit, Mastodon).  
b. Opciones:

- Seleccionar una cuenta existente para ver/gestionar sus tareas.
- Presionar el botón **“Agregar cuenta”** → va a la página de agregar cuenta.
- Presionar el botón **“Agregar tarea”** → va a la página de agregar tareas.

### 3. Agregar cuenta

a. El usuario selecciona la red social a vincular (ej: Instagram).  
b. Ingresa credenciales / token de API (dependiendo de la integración).  
c. El backend guarda en la base de datos la información encriptada o tokens de acceso.  
d. Redirige a la Mainpage, donde la nueva cuenta aparece en la lista.

### 4. Agregar tarea

a. El usuario selecciona la cuenta en la que quiere configurar una tarea.  
b. Al hacer clic en **“Agregar tarea”**, se abre la página de configuración:

- **Responder comentarios**:

  - Configura palabras clave → Respuesta asociada.
  - Ejemplo: Si alguien comenta “precio”, responder con “El producto cuesta $X”.

- **Publicaciones programadas**:

  - Subir imagen/texto.
  - Configurar fecha y hora de publicación.

- **Moderar comentarios** (solo una vez por cuenta, luego se desactiva):
  - Lista de palabras prohibidas.
  - Acción: Eliminar comentario.

c. El usuario guarda la tarea → se almacena en la base de datos asociada a esa cuenta.  
d. Redirige a la Mainpage, donde la tarea aparece en la lista de esa cuenta.

### 5. Ejecución manual de tareas

a. El backend (microservicio por red social) consulta las tareas almacenadas.  
b. El usuario puede presionar un botón **“Ejecutar ahora”** en la Mainpage.  
c. Según el tipo de tarea:

- **Responder comentarios** → Llama a la API de la red social, busca comentarios nuevos, y responde si coincide con alguna regla configurada.
- **Publicaciones programadas** → Publica si la fecha/hora es la actual o cercana.
- **Moderación** → Escanea comentarios nuevos y elimina si coinciden con la lista de insultos/spam.

---

## Arquitectura en AWS

a. Cada módulo será un microservicio:

- **Auth Service** → Manejo de login y hash.
- **Account Service** → Gestión de cuentas vinculadas.
- **Task Service** → CRUD de tareas.
- **Executor Service** → Ejecuta tareas contra las APIs de Instagram, Reddit, X.
- **Frontend (React o similar)** → UI.
- **Base de datos (RDS o DynamoDB)** → Almacena usuarios, cuentas y tareas.

---

## Diseño técnico

### 1. Auth Service

- Registro/login de usuarios.
- Hash de contraseñas con **SHA-512 + salt**.
- **JWT** para sesiones.

### 2. Account Service

- CRUD de cuentas vinculadas (Instagram, Reddit, Mastodon).
- Manejo seguro de tokens en **AWS Secrets Manager**.

### 3. Task Service

- CRUD de tareas: responder comentarios, programar publicaciones, moderar.
- Guarda la configuración en formato **JSON flexible (config_json)**.

### 4. Executor Service

- Ejecuta las tareas conectándose con APIs externas.
- Programación manual en Fase 1, luego con **scheduler (AWS EventBridge)**.

### 5. Frontend (React o Next.js)

- Login.
- Mainpage (cuentas + tareas).
- Agregar cuentas.
- Agregar tareas.
- Historial de ejecución (logs).

### 6. Base de datos (AWS RDS - PostgreSQL)

- users, accounts, tasks, logs.

### 7. Infraestructura en AWS

- **ECS (Fargate)** para contenedores (backend microservicios).
- **RDS (PostgreSQL)** como base de datos.
- **S3** para archivos multimedia de publicaciones.
- **CloudWatch** para logs y monitoreo.
- **Secrets Manager** para credenciales de APIs externas.

---

## Avances hasta ahora

Hasta ahora se tiene en funcionamiento los servicios de **auth_service** y **user_service** que fue una entrega anterior, además el frontend correspondiente al login.

### Estructura de los microservicios

```
CRUD_SOA/
├── auth_service/
│   └── app/
│       ├── auth/
│       │   ├── __init__.py
│       │   ├── dependencies.py
│       │   ├── models.py
│       │   ├── routes.py
│       │   └── utils.py
│       ├── tests/
│       │   └── __init__.py
│       ├── config.py
│       ├── create_admin.py
│       ├── database.py
│       ├── main.py
│       ├── schemas.py
│       ├── .env
│       ├── Dockerfile
│       └── requirements.txt
├── frontend/
│   ├── dashboard.html
│   ├── Dockerfile
│   ├── index.html
│   ├── main.js
│   └── styles.css
└── user_service/
    ├── app/
    │   ├── users/
    │   │   ├── __init__.py
    │   │   ├── dependencies.py
    │   │   └── routes.py
    │   ├── __init__.py
    │   ├── config.py
    │   ├── database.py
    │   ├── main.py
    │   ├── models.py
    │   └── schemas.py
    ├── tests/
    ├── .env
    ├── Dockerfile
    └── requirements.txt
```
