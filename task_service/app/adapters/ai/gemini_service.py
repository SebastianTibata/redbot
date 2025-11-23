# en app/adapters/ai/gemini_service.py

from app.domain.ports import AIGeneratorPort
from ...config import settings
import google.generativeai as genai
import json
import re
import logging

# ▼▼▼ PROMPT ACTUALIZADO ▼▼▼
SYSTEM_PROMPT = """
Eres un asistente que traduce peticiones en lenguaje natural a un formato JSON para un bot de Reddit.
Debes devolver SIEMPRE un objeto JSON con dos claves: "task_type" y "config".

Es CRÍTICO que uses los nombres de clave exactos para la 'config' como se describe a continuación:

1. task_type: "publicar"
   Config: {"subreddit": "...", "title": "...", "text": "..."}
   (Usa "subreddit", "title", y "text".)
   (Si el usuario NO especifica un subreddit o dice "mi perfil", simplemente OMITE la clave "subreddit".)

2. task_type: "responder"
   Config: {"post_url": "...", "keywords": ["...", "..."], "reply_text": "..."}

3. task_type: "moderar"
   Config: {"post_url": "...", "action": "remove", "filters": {"forbidden_words": ["...", "..."], "spam_patterns": ["...", "..."], "max_caps_percent": 70}}
   (Si el usuario pide "eliminar spam de links", usa "spam_patterns": ["http", "www"])
   (Si el usuario pide "eliminar comentarios que gritan", usa "max_caps_percent": 70)
   (Si el usuario solo da palabras, ponlas en "forbidden_words")

4. task_type: "validar_cuentas"
   Config: {}

5. task_type: "borrado_emergencia"
   Config: {"post_url": "..."}

Devuelve SÓLO el objeto JSON, sin texto adicional, explicaciones, o las marcas de "```json".
"""

class GeminiAIGenerator(AIGeneratorPort):
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(model_name="models/gemini-flash-latest")

    def generate_json_from_prompt(self, prompt: str) -> str:
        
        full_prompt = SYSTEM_PROMPT + "\n\nPETICIÓN DEL USUARIO: " + prompt
        
        try:
            response = self.model.generate_content(full_prompt)
            text_response = response.text
            
            match = re.search(r'\{.*\}', text_response, re.DOTALL)
            if not match:
                logging.error(f"La respuesta de la IA no era un JSON. Respuesta: {text_response}")
                raise ValueError("La respuesta de la IA no contenía un JSON válido.")
                
            json_string = match.group(0)
            json.loads(json_string) 
            
            logging.info(f"IA generó JSON exitosamente: {json_string}")
            return json_string
        
        except Exception as e:
            logging.error(f"Error llamando a Google Gemini: {e}")
            raise ValueError(f"Error al procesar el prompt de IA: {e}")