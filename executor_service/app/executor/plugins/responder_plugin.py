from ..plugin_interface import PluginInterface
import logging

class ResponderPlugin(PluginInterface):
    task_type = "responder"

    def execute(self, db_session, reddit_instance, task_config, account):
        logging.info(f"--- Ejecutando plugin de respuesta para el post: {task_config.get('post_url')} ---")
        post_url = task_config.get("post_url")
        keywords = task_config.get("keywords", [])
        reply_text = task_config.get("reply_text")

        if not all([post_url, keywords, reply_text]):
            raise ValueError("Configuración inválida para la tarea de respuesta.")

        submission = reddit_instance.submission(url=post_url)
        submission.comments.replace_more(limit=0)

        for comment in submission.comments.list():
            if comment.author and comment.author.name == reddit_instance.user.me().name:
                continue # No responder a nosotros mismos
            if any(keyword.lower() in comment.body.lower() for keyword in keywords):
                logging.info(f"Palabra clave encontrada en el comentario de '{comment.author}'. Respondiendo...")
                comment.reply(reply_text)
                logging.info("Respuesta enviada.")

        logging.info("--- Tarea de respuesta finalizada ---")