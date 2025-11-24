# Sistema de Seguridad RedBot

RedBot incluye un sistema de protección de acceso configurable que permite proteger la aplicación mediante llaves de acceso adicionales a la autenticación JWT estándar.

## Características

- **Autenticación simétrica**: Usa una llave maestra compartida
- **Autenticación asimétrica**: Usa criptografía de clave pública (RSA)
- **Configurable**: Puede habilitarse o deshabilitarse según las necesidades

## Configuración Inicial

### 1. Ejecutar el script de configuración

```bash
python setup_security.py
```

Este script le guiará a través de las opciones:

1. **Autenticación Simétrica (Llave Compartida)**
   - Genera o permite ingresar una llave maestra
   - Simple de usar pero menos segura
   - Ideal para desarrollo o aplicaciones internas

2. **Autenticación Asimétrica (RSA)**
   - Genera un par de claves pública/privada
   - Más segura, previene replay attacks
   - Ideal para producción

3. **Deshabilitar Autenticación Adicional**
   - Solo usa autenticación JWT estándar
   - Sin protección adicional

### 2. Aplicar la configuración

Después de ejecutar el script, copie el contenido de `.env.security` a su archivo `.env`:

```bash
cat .env.security >> .env
```

### 3. Reiniciar la aplicación

```bash
docker-compose down
docker-compose up -d
```

## Uso

### Autenticación Simétrica

Incluya el header `X-Master-Key` en cada request:

```bash
curl -H "X-Master-Key: su_llave_maestra_aqui" \
     -H "Authorization: Bearer <jwt_token>" \
     http://localhost:8000/api/accounts
```

### Autenticación Asimétrica

1. **Firmar un request:**

```bash
python sign_request.py "mi_usuario_123"
```

Esto generará un token y una firma.

2. **Usar el token y firma en su request:**

```bash
curl -H "X-Access-Token: <token>" \
     -H "X-Access-Signature: <signature>" \
     -H "Authorization: Bearer <jwt_token>" \
     http://localhost:8000/api/accounts
```

## Frontend

El frontend debe modificarse para incluir los headers de seguridad en cada request:

### Ejemplo con autenticación simétrica:

```javascript
const masterKey = localStorage.getItem('masterKey');
const token = localStorage.getItem('token');

fetch('/api/accounts', {
    headers: {
        'Authorization': `Bearer ${token}`,
        'X-Master-Key': masterKey
    }
});
```

### Ejemplo con autenticación asimétrica:

```javascript
// Obtener token y firma del servidor de autenticación
const { accessToken, accessSignature } = await getSignedAccess();
const token = localStorage.getItem('token');

fetch('/api/accounts', {
    headers: {
        'Authorization': `Bearer ${token}`,
        'X-Access-Token': accessToken,
        'X-Access-Signature': accessSignature
    }
});
```

## Rutas Excluidas

Las siguientes rutas NO requieren la llave de acceso adicional:

- `/docs` - Documentación de la API
- `/redoc` - Documentación alternativa
- `/openapi.json` - Especificación OpenAPI
- `/health` - Health check
- `/api/auth/login` - Login
- `/api/auth/register` - Registro

## Variables de Entorno

### Autenticación Simétrica

```env
APP_AUTH_TYPE=symmetric
APP_MASTER_KEY=su_llave_maestra_aqui
```

### Autenticación Asimétrica

```env
APP_AUTH_TYPE=asymmetric
APP_PRIVATE_KEY_PATH=./keys/private_key.pem
APP_PUBLIC_KEY_PATH=./keys/public_key.pem
APP_TOKEN_VALIDITY_MINUTES=60
```

### Deshabilitar

```env
APP_AUTH_TYPE=disabled
```

## Seguridad

### Autenticación Simétrica

- **Ventajas**: Simple de implementar y usar
- **Desventajas**:
  - La llave debe compartirse entre cliente y servidor
  - Vulnerable a replay attacks si no se usa HTTPS
  - Si la llave se compromete, debe cambiarse en todos los clientes

**Recomendaciones:**
- Use HTTPS siempre
- Rote la llave periódicamente
- No comparta la llave en repositorios públicos
- Use variables de entorno para almacenar la llave

### Autenticación Asimétrica

- **Ventajas**:
  - Más segura que la simétrica
  - La clave privada nunca se transmite
  - Incluye timestamp para prevenir replay attacks
  - Tokens tienen expiración configurable

- **Desventajas**:
  - Más compleja de implementar
  - Requiere generar y gestionar par de claves

**Recomendaciones:**
- Guarde la clave privada en un lugar seguro
- No comparta la clave privada
- Use permisos restrictivos en los archivos de claves (chmod 600)
- Configure un tiempo de validez corto para los tokens
- Implemente rotación de claves periódica

## Integración con Servicios

Para habilitar el middleware de seguridad en un servicio FastAPI:

```python
from shared.security_middleware import setup_security_middleware

app = FastAPI()

# Configurar middleware de seguridad
setup_security_middleware(app, exclude_paths=[
    '/docs',
    '/health',
    '/api/auth/login'
])
```

## Troubleshooting

### "Acceso denegado: llave maestra inválida o faltante"

- Verifique que está enviando el header `X-Master-Key`
- Verifique que la llave coincide con la configurada en `.env`
- Verifique que reinició la aplicación después de cambiar la configuración

### "Acceso denegado: token o firma inválida"

- Verifique que el token no haya expirado
- Regenere el token usando `sign_request.py`
- Verifique que las claves en el servidor son correctas
- Verifique que está enviando ambos headers: `X-Access-Token` y `X-Access-Signature`

### Los requests funcionan en Postman pero no en el frontend

- Verifique que el frontend está enviando los headers de seguridad
- Verifique la configuración de CORS
- Revise la consola del navegador en busca de errores
