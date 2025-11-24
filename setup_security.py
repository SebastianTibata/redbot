#!/usr/bin/env python3
"""
Script de configuración de seguridad para RedBot.
Permite configurar la protección de acceso a la aplicación.
"""

import os
import sys
import secrets
from shared.security_config import generate_rsa_keys


def setup_symmetric_auth():
    """Configura autenticación con llave simétrica."""
    print("\n=== Configuración de Autenticación Simétrica ===")
    print("La autenticación simétrica usa una llave maestra compartida.")
    print("Esta llave debe ser proporcionada en el header 'X-Master-Key' en cada request.")
    print()

    # Generar una llave aleatoria o permitir al usuario ingresar una
    choice = input("¿Desea generar una llave aleatoria? (s/n): ").lower()

    if choice == 's':
        master_key = secrets.token_urlsafe(32)
        print(f"\nLlave maestra generada: {master_key}")
    else:
        master_key = input("Ingrese su llave maestra: ")

    # Guardar en archivo .env
    env_path = '.env.security'
    with open(env_path, 'w') as f:
        f.write(f"APP_AUTH_TYPE=symmetric\n")
        f.write(f"APP_MASTER_KEY={master_key}\n")

    print(f"\n✓ Configuración guardada en {env_path}")
    print("\nPara usar esta configuración:")
    print("1. Copie el contenido de .env.security a su archivo .env")
    print("2. Reinicie la aplicación")
    print(f"3. En cada request, incluya el header: X-Master-Key: {master_key}")


def setup_asymmetric_auth():
    """Configura autenticación con clave asimétrica (RSA)."""
    print("\n=== Configuración de Autenticación Asimétrica (RSA) ===")
    print("La autenticación asimétrica usa un par de claves pública/privada.")
    print("El servidor usa la clave pública para verificar tokens firmados con la clave privada.")
    print()

    # Generar claves RSA
    keys_dir = input("Directorio para guardar las claves (default: ./keys): ").strip() or './keys'

    print("\nGenerando claves RSA...")
    private_key_path, public_key_path = generate_rsa_keys(keys_dir)

    # Guardar configuración en .env
    env_path = '.env.security'
    with open(env_path, 'w') as f:
        f.write(f"APP_AUTH_TYPE=asymmetric\n")
        f.write(f"APP_PRIVATE_KEY_PATH={private_key_path}\n")
        f.write(f"APP_PUBLIC_KEY_PATH={public_key_path}\n")
        f.write(f"APP_TOKEN_VALIDITY_MINUTES=60\n")

    print(f"\n✓ Claves generadas en {keys_dir}/")
    print(f"✓ Configuración guardada en {env_path}")
    print("\nPara usar esta configuración:")
    print("1. Copie el contenido de .env.security a su archivo .env")
    print("2. Guarde la clave privada en un lugar seguro")
    print("3. Reinicie la aplicación")
    print("4. Use la clave privada para firmar tokens antes de cada request")
    print("\nEjemplo de uso:")
    print("  python sign_request.py 'mi_usuario_123'")


def disable_auth():
    """Deshabilita la autenticación adicional."""
    print("\n=== Deshabilitar Autenticación Adicional ===")
    print("Esto deshabilitará la protección de llave maestra.")
    print("Solo se usará la autenticación JWT estándar.")
    print()

    confirm = input("¿Está seguro? (s/n): ").lower()
    if confirm != 's':
        print("Operación cancelada.")
        return

    env_path = '.env.security'
    with open(env_path, 'w') as f:
        f.write(f"APP_AUTH_TYPE=disabled\n")

    print(f"\n✓ Configuración guardada en {env_path}")
    print("La autenticación adicional ha sido deshabilitada.")


def main():
    print("=" * 60)
    print("RedBot - Configuración de Seguridad")
    print("=" * 60)
    print()
    print("Opciones:")
    print("1. Configurar autenticación simétrica (llave compartida)")
    print("2. Configurar autenticación asimétrica (RSA)")
    print("3. Deshabilitar autenticación adicional")
    print("4. Salir")
    print()

    choice = input("Seleccione una opción (1-4): ").strip()

    if choice == '1':
        setup_symmetric_auth()
    elif choice == '2':
        setup_asymmetric_auth()
    elif choice == '3':
        disable_auth()
    elif choice == '4':
        print("Saliendo...")
        sys.exit(0)
    else:
        print("Opción inválida.")
        sys.exit(1)


if __name__ == "__main__":
    main()
