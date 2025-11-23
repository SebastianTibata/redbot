# en executor_service/app/executor/plugins/emergency_delete_plugin.py
from ..plugin_interface import PluginInterface

class EmergencyDeletePlugin(PluginInterface):
    task_type = "borrado_emergencia"

    def execute(self, db_session, reddit_instance, task_config, account):
        print("--- Ejecutando Plugin de Borrado de Emergencia ---")
        post_url = task_config.get("post_url")
        if not post_url:
            raise ValueError("Se necesita 'post_url' en la configuración JSON.")

        bot_username = reddit_instance.user.me().name
        print(f"Buscando comentarios de '{bot_username}' en el post: {post_url}")

        submission = reddit_instance.submission(url=post_url)
        submission.comments.replace_more(limit=0)

        count = 0
        for comment in submission.comments.list():
            if comment.author and comment.author.name == bot_username:
                print(f"Eliminando comentario: '{comment.body[:30]}...'")
                comment.delete()
                count += 1

        print(f"--- Borrado de Emergencia Finalizado: {count} comentarios eliminados. ---")