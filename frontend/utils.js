/**
 * Utilidades para el frontend de RedBot
 * Maneja automáticamente la autenticación JWT y las llaves de seguridad
 */

// Configuración del sistema de seguridad
const SECURITY_CONFIG = {
    // Tipo de autenticación: 'symmetric', 'asymmetric', 'disabled'
    // Esta configuración debe coincidir con el backend
    authType: localStorage.getItem('securityAuthType') || 'disabled',

    // Para autenticación simétrica
    masterKey: localStorage.getItem('masterKey') || null,

    // Para autenticación asimétrica
    accessToken: localStorage.getItem('accessToken') || null,
    accessSignature: localStorage.getItem('accessSignature') || null
};

/**
 * Actualiza la configuración de seguridad
 */
function updateSecurityConfig(authType, credentials) {
    SECURITY_CONFIG.authType = authType;
    localStorage.setItem('securityAuthType', authType);

    if (authType === 'symmetric' && credentials.masterKey) {
        SECURITY_CONFIG.masterKey = credentials.masterKey;
        localStorage.setItem('masterKey', credentials.masterKey);
    } else if (authType === 'asymmetric' && credentials.accessToken && credentials.accessSignature) {
        SECURITY_CONFIG.accessToken = credentials.accessToken;
        SECURITY_CONFIG.accessSignature = credentials.accessSignature;
        localStorage.setItem('accessToken', credentials.accessToken);
        localStorage.setItem('accessSignature', credentials.accessSignature);
    }
}

/**
 * Limpia la configuración de seguridad
 */
function clearSecurityConfig() {
    localStorage.removeItem('securityAuthType');
    localStorage.removeItem('masterKey');
    localStorage.removeItem('accessToken');
    localStorage.removeItem('accessSignature');
    SECURITY_CONFIG.authType = 'disabled';
    SECURITY_CONFIG.masterKey = null;
    SECURITY_CONFIG.accessToken = null;
    SECURITY_CONFIG.accessSignature = null;
}

/**
 * Construye los headers de autenticación
 * Incluye JWT y headers de seguridad según la configuración
 */
function getAuthHeaders() {
    const headers = {
        'Content-Type': 'application/json'
    };

    // Agregar JWT token si existe
    const token = localStorage.getItem('token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    // Agregar headers de seguridad según el tipo
    if (SECURITY_CONFIG.authType === 'symmetric' && SECURITY_CONFIG.masterKey) {
        headers['X-Master-Key'] = SECURITY_CONFIG.masterKey;
    } else if (SECURITY_CONFIG.authType === 'asymmetric') {
        if (SECURITY_CONFIG.accessToken && SECURITY_CONFIG.accessSignature) {
            headers['X-Access-Token'] = SECURITY_CONFIG.accessToken;
            headers['X-Access-Signature'] = SECURITY_CONFIG.accessSignature;
        }
    }

    return headers;
}

/**
 * Función helper para hacer requests seguros con autenticación automática
 *
 * @param {string} url - URL del endpoint
 * @param {object} options - Opciones de fetch (method, body, etc.)
 * @returns {Promise<Response>}
 */
async function secureFetch(url, options = {}) {
    // Construir headers combinando los de autenticación con los proporcionados
    const headers = {
        ...getAuthHeaders(),
        ...(options.headers || {})
    };

    // Hacer el request
    const response = await fetch(url, {
        ...options,
        headers
    });

    // Si recibimos 401 o 403, redirigir al login
    if (response.status === 401) {
        alert('Sesión expirada. Por favor, inicie sesión nuevamente.');
        localStorage.removeItem('token');
        window.location.href = 'login.html';
        return response;
    }

    // Si recibimos 403 por llave de seguridad inválida
    if (response.status === 403) {
        const error = await response.json().catch(() => ({}));
        if (error.auth_type) {
            alert(`Error de autenticación: ${error.detail}\n\nTipo requerido: ${error.auth_type}`);
            // Mostrar modal de configuración de seguridad
            showSecurityConfigModal();
        }
        return response;
    }

    return response;
}

/**
 * Muestra un modal para configurar las credenciales de seguridad
 */
function showSecurityConfigModal() {
    const existingModal = document.getElementById('securityModal');
    if (existingModal) {
        existingModal.style.display = 'block';
        return;
    }

    const modal = document.createElement('div');
    modal.id = 'securityModal';
    modal.innerHTML = `
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 10000;">
            <div style="background: white; padding: 30px; border-radius: 10px; max-width: 500px; width: 90%;">
                <h2 style="margin-top: 0;">Configuración de Seguridad</h2>
                <p>Este sistema requiere credenciales de seguridad adicionales.</p>

                <label for="authTypeSelect" style="display: block; margin-top: 15px; font-weight: bold;">Tipo de autenticación:</label>
                <select id="authTypeSelect" style="width: 100%; padding: 10px; margin-top: 5px; border-radius: 5px; border: 1px solid #ccc;">
                    <option value="disabled">Deshabilitada (sin protección adicional)</option>
                    <option value="symmetric">Simétrica (llave compartida)</option>
                    <option value="asymmetric">Asimétrica (firma digital)</option>
                </select>

                <div id="symmetricFields" style="display: none; margin-top: 15px;">
                    <label style="display: block; font-weight: bold;">Llave Maestra:</label>
                    <input type="password" id="masterKeyInput" placeholder="Ingrese la llave maestra" style="width: 100%; padding: 10px; margin-top: 5px; border-radius: 5px; border: 1px solid #ccc;">
                </div>

                <div id="asymmetricFields" style="display: none; margin-top: 15px;">
                    <label style="display: block; font-weight: bold;">Access Token:</label>
                    <input type="text" id="accessTokenInput" placeholder="Token de acceso" style="width: 100%; padding: 10px; margin-top: 5px; margin-bottom: 10px; border-radius: 5px; border: 1px solid #ccc;">

                    <label style="display: block; font-weight: bold;">Access Signature:</label>
                    <input type="text" id="accessSignatureInput" placeholder="Firma de acceso" style="width: 100%; padding: 10px; margin-top: 5px; border-radius: 5px; border: 1px solid #ccc;">

                    <p style="margin-top: 10px; font-size: 0.9em; color: #666;">
                        Genere el token y firma usando: <code style="background: #f0f0f0; padding: 2px 6px; border-radius: 3px;">python sign_request.py "datos"</code>
                    </p>
                </div>

                <div style="margin-top: 20px; display: flex; gap: 10px;">
                    <button id="saveSecurityBtn" style="flex: 1; padding: 12px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 1em;">
                        Guardar
                    </button>
                    <button id="cancelSecurityBtn" style="flex: 1; padding: 12px; background: #ccc; color: #333; border: none; border-radius: 5px; cursor: pointer; font-size: 1em;">
                        Cancelar
                    </button>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    // Manejar cambio de tipo de autenticación
    const authTypeSelect = document.getElementById('authTypeSelect');
    const symmetricFields = document.getElementById('symmetricFields');
    const asymmetricFields = document.getElementById('asymmetricFields');

    authTypeSelect.value = SECURITY_CONFIG.authType;
    updateFieldsVisibility();

    authTypeSelect.addEventListener('change', updateFieldsVisibility);

    function updateFieldsVisibility() {
        const authType = authTypeSelect.value;
        symmetricFields.style.display = authType === 'symmetric' ? 'block' : 'none';
        asymmetricFields.style.display = authType === 'asymmetric' ? 'block' : 'none';
    }

    // Pre-llenar con valores existentes
    if (SECURITY_CONFIG.masterKey) {
        document.getElementById('masterKeyInput').value = SECURITY_CONFIG.masterKey;
    }
    if (SECURITY_CONFIG.accessToken) {
        document.getElementById('accessTokenInput').value = SECURITY_CONFIG.accessToken;
    }
    if (SECURITY_CONFIG.accessSignature) {
        document.getElementById('accessSignatureInput').value = SECURITY_CONFIG.accessSignature;
    }

    // Guardar configuración
    document.getElementById('saveSecurityBtn').addEventListener('click', () => {
        const authType = authTypeSelect.value;

        if (authType === 'symmetric') {
            const masterKey = document.getElementById('masterKeyInput').value;
            if (!masterKey) {
                alert('Por favor, ingrese la llave maestra.');
                return;
            }
            updateSecurityConfig('symmetric', { masterKey });
        } else if (authType === 'asymmetric') {
            const accessToken = document.getElementById('accessTokenInput').value;
            const accessSignature = document.getElementById('accessSignatureInput').value;
            if (!accessToken || !accessSignature) {
                alert('Por favor, ingrese el token y la firma de acceso.');
                return;
            }
            updateSecurityConfig('asymmetric', { accessToken, accessSignature });
        } else {
            updateSecurityConfig('disabled', {});
        }

        modal.style.display = 'none';
        alert('Configuración de seguridad actualizada. Recargue la página para aplicar los cambios.');
        location.reload();
    });

    // Cancelar
    document.getElementById('cancelSecurityBtn').addEventListener('click', () => {
        modal.style.display = 'none';
    });
}

/**
 * Función de logout mejorada
 */
function logout() {
    localStorage.removeItem('token');
    clearSecurityConfig();
    window.location.href = 'login.html';
}

// Agregar botón de configuración de seguridad en la navegación (opcional)
document.addEventListener('DOMContentLoaded', () => {
    // Agregar indicador visual del estado de seguridad
    const nav = document.querySelector('nav');
    if (nav && SECURITY_CONFIG.authType !== 'disabled') {
        const indicator = document.createElement('span');
        indicator.style.cssText = 'position: fixed; top: 10px; right: 10px; background: #4caf50; color: white; padding: 5px 10px; border-radius: 5px; font-size: 0.8em; z-index: 1000; cursor: pointer;';
        indicator.textContent = `🔒 Seguridad: ${SECURITY_CONFIG.authType}`;
        indicator.title = 'Click para configurar';
        indicator.addEventListener('click', showSecurityConfigModal);
        document.body.appendChild(indicator);
    }
});
