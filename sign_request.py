#!/usr/bin/env python3
"""
Utilidad para firmar requests cuando se usa autenticación asimétrica.
"""

import sys
import os
from datetime import datetime

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shared.security_config import SecurityConfig


def main():
    if len(sys.argv) < 2:
        print("Uso: python sign_request.py <datos_a_firmar>")
        print("\nEjemplo:")
        print("  python sign_request.py 'mi_usuario_123'")
        sys.exit(1)

    data = sys.argv[1]

    # Cargar configuración de seguridad
    config = SecurityConfig()

    if config.auth_type != 'asymmetric':
        print("Error: La autenticación asimétrica no está configurada.")
        print("Ejecute 'python setup_security.py' primero.")
        sys.exit(1)

    try:
        # Firmar el token
        token, signature = config.sign_token(data)

        print("=" * 60)
        print("Token firmado correctamente")
        print("=" * 60)
        print(f"\nToken:     {token}")
        print(f"Signature: {signature}")
        print("\nHeaders para incluir en su request:")
        print(f"  X-Access-Token: {token}")
        print(f"  X-Access-Signature: {signature}")
        print("\nEjemplo con curl:")
        print(f"  curl -H 'X-Access-Token: {token}' \\")
        print(f"       -H 'X-Access-Signature: {signature}' \\")
        print(f"       -H 'Authorization: Bearer <jwt_token>' \\")
        print("       http://localhost:8000/api/accounts")

    except Exception as e:
        print(f"Error al firmar el token: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
