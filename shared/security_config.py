"""
Sistema de protección de acceso a la aplicación RedBot.
Soporta autenticación con llave simétrica (clave compartida) o asimétrica (RSA).
"""

import os
import hashlib
import hmac
from typing import Optional, Literal
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta

class SecurityConfig:
    """
    Configuración de seguridad para la aplicación.
    Permite proteger el acceso mediante claves simétricas o asimétricas.
    """

    def __init__(self):
        # Tipo de autenticación: 'symmetric', 'asymmetric', o 'disabled'
        self.auth_type: Literal['symmetric', 'asymmetric', 'disabled'] = os.getenv('APP_AUTH_TYPE', 'disabled')

        # Para autenticación simétrica
        self.master_key: Optional[str] = os.getenv('APP_MASTER_KEY', None)

        # Para autenticación asimétrica
        self.private_key_path: str = os.getenv('APP_PRIVATE_KEY_PATH', './keys/private_key.pem')
        self.public_key_path: str = os.getenv('APP_PUBLIC_KEY_PATH', './keys/public_key.pem')

        # Tiempo de validez de tokens firmados (en minutos)
        self.token_validity_minutes: int = int(os.getenv('APP_TOKEN_VALIDITY_MINUTES', '60'))

    def verify_symmetric_key(self, provided_key: str) -> bool:
        """
        Verifica que la llave proporcionada coincida con la llave maestra.
        Usa comparación segura para evitar timing attacks.
        """
        if not self.master_key:
            return False

        # Usar hmac.compare_digest para comparación segura
        return hmac.compare_digest(provided_key, self.master_key)

    def verify_signed_token(self, token: str, signature: str) -> bool:
        """
        Verifica un token firmado con la clave privada.
        El token debe incluir un timestamp para evitar replay attacks.
        """
        try:
            # Cargar la clave pública
            with open(self.public_key_path, 'rb') as key_file:
                public_key = serialization.load_pem_public_key(
                    key_file.read(),
                    backend=default_backend()
                )

            # Verificar la firma
            public_key.verify(
                bytes.fromhex(signature),
                token.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            # Verificar el timestamp en el token
            # Formato esperado: "timestamp:user_id:random_data"
            parts = token.split(':')
            if len(parts) < 1:
                return False

            token_timestamp = int(parts[0])
            current_timestamp = int(datetime.now().timestamp())

            # Verificar que el token no haya expirado
            if current_timestamp - token_timestamp > self.token_validity_minutes * 60:
                return False

            return True
        except Exception as e:
            print(f"Error verificando token firmado: {e}")
            return False

    def sign_token(self, data: str) -> tuple[str, str]:
        """
        Firma un token con la clave privada.
        Retorna (token, signature).
        """
        try:
            # Crear token con timestamp
            timestamp = int(datetime.now().timestamp())
            token = f"{timestamp}:{data}"

            # Cargar la clave privada
            with open(self.private_key_path, 'rb') as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )

            # Firmar el token
            signature = private_key.sign(
                token.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            return token, signature.hex()
        except Exception as e:
            print(f"Error firmando token: {e}")
            raise

    def is_enabled(self) -> bool:
        """Retorna True si la protección de acceso está habilitada."""
        return self.auth_type != 'disabled'

    def verify_access(self, provided_key: Optional[str] = None,
                     token: Optional[str] = None,
                     signature: Optional[str] = None) -> bool:
        """
        Verifica el acceso según el tipo de autenticación configurado.

        Args:
            provided_key: Llave proporcionada para autenticación simétrica
            token: Token para autenticación asimétrica
            signature: Firma del token para autenticación asimétrica

        Returns:
            True si el acceso es válido, False en caso contrario
        """
        if self.auth_type == 'disabled':
            return True

        if self.auth_type == 'symmetric':
            if not provided_key:
                return False
            return self.verify_symmetric_key(provided_key)

        if self.auth_type == 'asymmetric':
            if not token or not signature:
                return False
            return self.verify_signed_token(token, signature)

        return False


def generate_rsa_keys(output_dir: str = './keys'):
    """
    Genera un par de claves RSA para autenticación asimétrica.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Generar clave privada
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Guardar clave privada
    private_key_path = os.path.join(output_dir, 'private_key.pem')
    with open(private_key_path, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Generar y guardar clave pública
    public_key = private_key.public_key()
    public_key_path = os.path.join(output_dir, 'public_key.pem')
    with open(public_key_path, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print(f"Claves generadas en {output_dir}/")
    print(f"  - Clave privada: {private_key_path}")
    print(f"  - Clave pública: {public_key_path}")

    return private_key_path, public_key_path


# Instancia global de configuración
security_config = SecurityConfig()
