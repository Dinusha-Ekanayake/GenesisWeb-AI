from typing import Dict
from ..interfaces.plugin import Plugin
from ..exceptions.errors import PluginRegistrationError

class PluginRegistry:
    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> None:
        if plugin.name in self._plugins:
            raise PluginRegistrationError(f"Plugin {plugin.name} is already registered.")
        self._plugins[plugin.name] = plugin

    def get_plugin(self, name: str) -> Plugin:
        if name not in self._plugins:
            raise PluginRegistrationError(f"Plugin {name} not found.")
        return self._plugins[name]
        
    def list_plugins(self) -> list[str]:
        return list(self._plugins.keys())
