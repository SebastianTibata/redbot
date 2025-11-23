# en executor_service/app/executor/plugins/publicar_plugin.py

from ..plugin_interface import PluginInterface
import logging

class PublicarPlugin(PluginInterface):
    """
    Este plugin maneja la lógica para crear una nueva publicación en Reddit.
    Si no se provee un subreddit, publicará en el perfil del usuario.
    """
    task_type = "publicar"

    def execute(self, db_session, reddit_instance, task_config, account):
        logging.info(f"Ejecutando plugin de 'publicar' para la cuenta {account.handle}")

        # 1. Obtener la configuración de la tarea
        subreddit_name = task_config.get("subreddit") # Puede ser None o ""
        title = task_config.get("title")
        text = task_config.get("text")

        # 2. Lógica de default (¡NUEVO!)
        if not subreddit_name:
            subreddit_name = f"u_{account.handle}"
            logging.info(f"No se especificó subreddit. Usando perfil del usuario por defecto: {subreddit_name}")

        # 3. Validar que la configuración esté completa (ahora solo title y text)
        if not all([title, text]):
            raise ValueError("Configuración incompleta para 'publicar'. Faltan 'title' o 'text'.")

        try:
            # 4. Obtener el objeto subreddit desde PRAW
            subreddit = reddit_instance.subreddit(subreddit_name)

            # 5. Realizar la publicación
            logging.info(f"Publicando en '{subreddit_name}' con el título '{title}'...")
            submission = subreddit.submit(title, selftext=text)
            
            logging.info(f"¡Publicación exitosa! URL: {submission.url}")

        except Exception as e:
            logging.error(f"Error al publicar en '{subreddit_name}': {e}")
            # Relanzamos el error para que el worker la marque como 'failed'
            raise e