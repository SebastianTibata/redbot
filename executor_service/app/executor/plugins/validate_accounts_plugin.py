# en executor_service/app/executor/plugins/validate_accounts_plugin.py
from ..plugin_interface import PluginInterface
from ... import models # Importa los modelos desde 'app'

class ValidateAccountsPlugin(PluginInterface):
    task_type = "validar_cuentas"

    def execute(self, db_session, reddit_instance, task_config, account):
        print("--- Ejecutando Plugin de Validación de Cuentas ---")

        # Para esta tarea, la instancia de reddit_instance no se usa,
        # ya que necesitamos crear una nueva por cada cuenta a validar.

        cuentas_a_validar = db_session.query(models.Account).all()
        for cuenta in cuentas_a_validar:
            print(f"Validando cuenta ID={cuenta.id}, Handle='{cuenta.handle}'...")
            try:
                # Creamos una instancia de PRAW específica para esta cuenta
                # Esta lógica debe estar en un lugar accesible, como un archivo 'utils'
                # Por ahora, la replicamos aquí para el ejemplo.
                from ..reddit_bot import get_reddit_instance
                reddit = get_reddit_instance(cuenta.token)

                # La prueba definitiva: ¿podemos obtener el usuario?
                if reddit.user.me():
                    print(f"-> Cuenta '{cuenta.handle}' está ACTIVA.")
                else:
                    # En un caso real, aquí podrías actualizar el estado de la cuenta en la BD
                    print(f"-> Cuenta '{cuenta.handle}' podría estar INACTIVA (autenticación silenciosa fallida).")

            except Exception as e:
                # Si get_reddit_instance falla, el token es inválido
                print(f"-> Cuenta '{cuenta.handle}' está INACTIVA (Error: {e}).")

        print("--- Validación de Cuentas Finalizada ---")