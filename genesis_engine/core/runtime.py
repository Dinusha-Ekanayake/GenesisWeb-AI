from ..plugins.registry import PluginRegistry
from ..rules.registry import RuleRegistry
import logging

class Runtime:
    """
    Internal Runtime class responsible for lifecycle management,
    dependency injection, logging, and module registration.
    """
    def __init__(self):
        self.plugin_registry = PluginRegistry()
        self.rule_registry = RuleRegistry()
        self.logger = logging.getLogger("GenesisRuntime")
        
        self._initialize_logging()

    def _initialize_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger.info("GenesisRuntime initialized.")

    def register_plugin(self, plugin):
        self.plugin_registry.register(plugin)
        self.logger.info(f"Registered plugin: {plugin.name}")

    def shutdown(self):
        self.logger.info("GenesisRuntime shutting down.")
