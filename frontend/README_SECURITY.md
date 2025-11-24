# Sistema de Seguridad Automático - Frontend

Este documento explica cómo funciona la integración automática del sistema de seguridad en el frontend.

## Arquitectura

El sistema de seguridad funciona de manera transparente y automática mediante:

1. **utils.js**: Biblioteca de utilidades que maneja la autenticación
2. **secureFetch()**: Función helper que reemplaza fetch() estándar
3. **Configuración en localStorage**: Almacena credenciales de seguridad

## Flujo de Autenticación

### 1. Login

Cuando un usuario inicia sesión en `index.html`:

```
Usuario ingresa credenciales → Login → (Opcional) Configura seguridad → Credenciales guardadas en localStorage
```

Las credenciales se pueden configurar en el login expandiendo la sección "Configuración de Seguridad (Opcional)".

**Tipos de configuración:**
- **Deshabilitada**: Solo usa JWT (por defecto)
- **Simétrica**: Requiere llave maestra compartida
- **Asimétrica**: Requiere token y firma digital

### 2. Requests Automáticos

Todos los archivos JS del frontend usan `secureFetch()` en lugar de `fetch()`:

```javascript
// Antes (sin seguridad automática)
const res = await fetch('/api/accounts', {
    headers: { 'Authorization': `Bearer ${token}` }
});

// Ahora (con seguridad automática)
const res = await secureFetch('/api/accounts');
```

`secureFetch()` automáticamente:
1. Lee las credenciales de localStorage
2. Agrega el token JWT
3. Agrega headers de seguridad según la configuración
4. Maneja errores 401/403 automáticamente

### 3. Headers Automáticos

Según la configuración, `secureFetch()` agrega estos headers:

#### Autenticación Deshabilitada
```
Authorization: Bearer <jwt_token>
```

#### Autenticación Simétrica
```
Authorization: Bearer <jwt_token>
X-Master-Key: <llave_maestra>
```

#### Autenticación Asimétrica
```
Authorization: Bearer <jwt_token>
X-Access-Token: <token>
X-Access-Signature: <firma>
```

## Archivos Modificados

### Archivos Principales
- `utils.js` - Biblioteca de seguridad
- `main.js` - Usa secureFetch()
- `metrics.js` - Usa secureFetch()
- `login.js` - Guarda configuración de seguridad
- `index.html` - Formulario de configuración

### Archivos HTML
Todos los archivos HTML incluyen `utils.js` antes de su script específico:

```html
<script src="utils.js"></script>
<script src="main.js"></script>
```

## Uso para Usuarios

### Opción 1: Sin Seguridad Adicional (Por Defecto)

1. Inicie sesión normalmente
2. No configure nada en "Configuración de Seguridad"
3. La app funcionará solo con JWT

### Opción 2: Con Llave Simétrica

1. Obtenga la llave maestra del administrador
2. En el login, expanda "Configuración de Seguridad (Opcional)"
3. Seleccione "Simétrica (llave compartida)"
4. Ingrese la llave maestra
5. Inicie sesión

La llave se guardará automáticamente y se usará en todos los requests.

### Opción 3: Con Firma Digital (Asimétrica)

1. Genere token y firma usando:
   ```bash
   python sign_request.py "mi_usuario"
   ```

2. En el login, expanda "Configuración de Seguridad (Opcional)"
3. Seleccione "Asimétrica (firma digital)"
4. Ingrese el token y la firma
5. Inicie sesión

**Nota:** Los tokens expiran según la configuración del servidor (por defecto 60 minutos).

## Modal de Configuración

Si un request falla por falta de credenciales de seguridad (403), se muestra automáticamente un modal para configurarlas:

```
Request → 403 Forbidden → Modal aparece → Usuario configura → Request se reintenta
```

El modal permite:
- Cambiar el tipo de autenticación
- Actualizar credenciales
- Ver información sobre cada tipo

## Indicador de Seguridad

Cuando la seguridad está habilitada, aparece un indicador verde en la esquina superior derecha:

```
🔒 Seguridad: symmetric
```

Al hacer clic en él, se abre el modal de configuración.

## Manejo de Errores

### Error 401 (No autorizado)
- Token JWT expirado o inválido
- Redirige automáticamente al login
- Limpia localStorage

### Error 403 (Acceso denegado)
- Credenciales de seguridad inválidas o faltantes
- Muestra modal de configuración
- Permite actualizar credenciales sin perder sesión

### Error 502 (Bad Gateway)
- Servicio caído
- Muestra mensaje específico
- No redirige al login

## Funciones Principales en utils.js

### `secureFetch(url, options)`
Reemplazo de fetch() con autenticación automática.

```javascript
const res = await secureFetch('/api/tasks/', {
    method: 'POST',
    body: JSON.stringify(data)
});
```

### `getAuthHeaders()`
Construye headers de autenticación según la configuración.

```javascript
const headers = getAuthHeaders();
// Retorna: { 'Authorization': '...', 'X-Master-Key': '...' }
```

### `updateSecurityConfig(authType, credentials)`
Actualiza la configuración de seguridad.

```javascript
updateSecurityConfig('symmetric', { masterKey: 'abc123' });
```

### `showSecurityConfigModal()`
Muestra el modal de configuración de seguridad.

```javascript
showSecurityConfigModal(); // Abre el modal
```

### `logout()`
Cierra sesión y limpia todas las credenciales.

```javascript
logout(); // Limpia JWT y credenciales de seguridad
```

## Ventajas del Sistema

1. **Transparente**: Los desarrolladores solo usan `secureFetch()`
2. **Automático**: No necesita configuración manual en cada request
3. **Flexible**: Soporta 3 modos de autenticación
4. **User-friendly**: Modal automático para configurar credenciales
5. **Seguro**: Almacena credenciales en localStorage (mejor que hardcodear)
6. **Manejo de errores**: Detecta y maneja errores automáticamente

## Seguridad de localStorage

Las credenciales se almacenan en localStorage del navegador:

- **Ventaja**: Persisten entre sesiones
- **Desventaja**: Accesibles por JavaScript (XSS)

**Recomendaciones:**
- Use HTTPS siempre
- Rote credenciales periódicamente
- No comparta credenciales
- Cierre sesión al terminar

## Desarrollo

Para agregar seguridad automática a una nueva página:

1. Incluya `utils.js` en el HTML:
   ```html
   <script src="utils.js"></script>
   <script src="mi_script.js"></script>
   ```

2. Use `secureFetch()` en lugar de `fetch()`:
   ```javascript
   const res = await secureFetch('/api/endpoint');
   ```

¡Eso es todo! El sistema maneja todo automáticamente.
