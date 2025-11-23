# en executor_service/app/executor/plugin_interface.py
from abc import ABC, abstractmethod

class PluginInterface(ABC):
    """
    Todos los plugins deben heredar de esta clase.
    Define el contrato que el Kernel espera.
    """

    # El nombre de la tarea que este plugin puede manejar
    task_type = "nombre_de_tarea_a_manejar"

    @abstractmethod
    def execute(self, db_session, reddit_instance, task_config, account):
        """
        El método principal que el kernel llamará.
        Contiene toda la lógica del plugin.
        """
        pass