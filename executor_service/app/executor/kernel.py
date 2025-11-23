# en executor_service/app/executor/kernel.py
import os
import importlib
from .plugin_interface import PluginInterface

class Kernel:
    def __init__(self):
        self.plugins = {}
        self._load_plugins()

    def _load_plugins(self):
        """
        Escanea el directorio de plugins, los importa y los registra.
        """
        plugin_dir = os.path.join(os.path.dirname(__file__), "plugins")
        print(f"Cargando plugins desde: {plugin_dir}")

        for filename in os.listdir(plugin_dir):
            if filename.endswith("_plugin.py"):
                module_name = f"app.executor.plugins.{filename[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    for item_name in dir(module):
                        item = getattr(module, item_name)
                        if isinstance(item, type) and issubclass(item, PluginInterface) and item is not PluginInterface:
                            plugin_instance = item()
                            self.plugins[plugin_instance.task_type] = plugin_instance
                            print(f"-> Plugin '{plugin_instance.task_type}' cargado exitosamente.")
                except Exception as e:
                    print(f"ERROR al cargar el plugin {module_name}: {e}")

    def get_plugin(self, task_type: str):
        """
        Devuelve el plugin registrado para un tipo de tarea.
        """
        plugin = self.plugins.get(task_type)
        if not plugin:
            raise NotImplementedError(f"No hay un plugin que maneje el tipo de tarea '{task_type}'.")
        return plugin