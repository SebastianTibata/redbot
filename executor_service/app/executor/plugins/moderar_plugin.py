# en executor_service/app/executor/plugins/moderar_plugin.py

from ..plugin_interface import PluginInterface
import logging
import re

# --- (Las funciones de ayuda check_caps_percent, check_spam_patterns, etc. van aquí) ---
def check_caps_percent(text: str, percent_limit: int) -> bool:
    if not text: return False
    uppercase_chars = sum(1 for c in text if c.isupper())
    total_chars = sum(1 for c in text if c.isalpha())
    if total_chars == 0: return False
    percent = (uppercase_chars / total_chars) * 100
    return percent > percent_limit

def check_spam_patterns(text: str, patterns: list) -> bool:
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def check_forbidden_words(text: str, words: list) -> bool:
    text_lower = text.lower()
    return any(word.lower() in text_lower for word in words)
# --- (Fin de las funciones de ayuda) ---


class ModerarPlugin(PluginInterface):
    task_type = "moderar"

    def execute(self, db_session, reddit_instance, task_config, account):
        logging.info("--- Iniciando plugin de moderación ---")

        authenticated_user = reddit_instance.user.me()
        post_url = task_config.get("post_url")
        action = task_config.get("action", "remove")
        filters = task_config.get("filters", {})
        
        forbidden_words = filters.get("forbidden_words", [])
        spam_patterns = filters.get("spam_patterns", [])
        max_caps_percent = filters.get("max_caps_percent", 100)

        if not post_url:
            raise ValueError("Configuración inválida: falta 'post_url'.")

        submission = reddit_instance.submission(url=post_url)
        subreddit = submission.subreddit
        
        logging.info(f"Verificando permisos de moderador en 'r/{subreddit.display_name}'...")
        moderators = [str(mod) for mod in subreddit.moderator()]
        
        if authenticated_user.name not in moderators:
            logging.warning(f"El usuario NO es moderador. Abortando tarea.")
            raise Exception(f"El usuario {authenticated_user.name} no es moderador.")

        logging.info(f"✅ Permisos confirmados. Aplicando filtros...")
        submission.comments.replace_more(limit=0)
        
        # ▼▼▼ LÓGICA CORREGIDA ▼▼▼
        
        comments_to_delete = [] # 1. Crear una lista vacía
        
        # 2. PRIMER BUCLE: Encontrar todos los comentarios infractores
        logging.info("Buscando todos los comentarios que violan las reglas...")
        for comment in submission.comments.list():
            if comment.author and comment.author.name == authenticated_user.name:
                continue 

            reason = None
            
            if forbidden_words and check_forbidden_words(comment.body, forbidden_words):
                reason = "Palabra prohibida detectada"
            elif spam_patterns and check_spam_patterns(comment.body, spam_patterns):
                reason = "Patrón de spam detectado"
            elif max_caps_percent < 100 and check_caps_percent(comment.body, max_caps_percent):
                reason = f"Exceso de mayúsculas (>{max_caps_percent}%)"

            if reason:
                logging.info(f"Comentario de '{comment.author}' activó un filtro: {reason}")
                comments_to_delete.append(comment) # Añadir a la lista de borrado

        # 3. SEGUNDO BUCLE: Borrar todos los comentarios de la lista
        if not comments_to_delete:
            logging.info("No se encontraron comentarios que violen las reglas.")
        else:
            logging.info(f"Se encontraron {len(comments_to_delete)} comentarios para eliminar. Procediendo...")
            for comment in comments_to_delete:
                if action == "remove":
                    try:
                        comment.delete()
                        logging.info(f"-> Acción: Comentario de '{comment.author}' eliminado.")
                    except Exception as e:
                        logging.error(f"Error al eliminar el comentario {comment.id}: {e}")
        
        logging.info("--- Tarea de moderación finalizada ---")